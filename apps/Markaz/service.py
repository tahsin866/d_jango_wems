import redis
import json
from django.db import transaction, connection
from django.conf import settings
from django.utils import timezone
import pytz
from urllib.parse import urlparse

from apps.school.models import School
from apps.Markaz.models import MarkazApplication, MainMadrasaInfo, AssociatedMadrasa, Attachment, MadrashaCenter
from apps.Markaz.serializers import (
    SchoolSelectSerializer, MarkazApplicationSerializer, MainMadrasaInfoSerializer,
    AssociatedMadrasaSerializer, AttachmentSerializer
)
from apps.admin.CentralExam.models import ExamSetup
from apps.users.models import User, UserSessions, UserInformation

def get_redis_connection():
    """Get Redis connection from Django settings"""
    try:
        redis_url = getattr(settings, 'REDIS_URL', 'redis://localhost:6379/0')
        parsed_url = urlparse(redis_url)
        return redis.Redis(
            host=parsed_url.hostname,
            port=parsed_url.port,
            db=int(parsed_url.path.lstrip('/')) if parsed_url.path else 0,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5
        )
    except Exception as e:
        print(f"Redis connection error: {e}")
        return None

BN_MONTHS = [
    'জানুয়ারি', 'ফেব্রুয়ারি', 'মার্চ', 'এপ্রিল', 'মে', 'জুন',
    'জুলাই', 'আগস্ট', 'সেপ্টেম্বর', 'অক্টোবর', 'নভেম্বর', 'ডিসেম্বর'
]

def format_bangla_date(dt):
    if not dt:
        return ''
    dt = dt.astimezone(pytz.timezone('Asia/Dhaka'))
    return f"{dt.day} {BN_MONTHS[dt.month - 1]}, {dt.year}"

# Auth helpers
def extract_user_from_token(request):
    session_token = (
        request.headers.get('Authorization') or
        request.META.get('HTTP_AUTHORIZATION') or
        ''
    ).replace('Bearer ', '')
    user_obj = None
    if session_token:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT user_id, expires_at FROM user_sessions WHERE session_token = %s AND is_active = TRUE
            """, [session_token])
            row = cursor.fetchone()
            if row:
                user_id, expires_at = row
                now = timezone.now()
                if expires_at:
                    if timezone.is_naive(expires_at):
                        expires_at = timezone.make_aware(expires_at, timezone.get_default_timezone())
                    if expires_at < now:
                        return None, 'Session expired'
                try:
                    user_obj = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    return None, 'User not found'
    return user_obj, None

def check_madrasha_user(user_obj):
    user_type_name = getattr(getattr(user_obj, 'user_type', None), 'name', None)
    if not user_type_name or user_type_name.strip().lower() != 'madrasha':
        return False
    return True

def create_markaz_application(data, user_obj):
    with transaction.atomic():
        try:
            user_info = UserInformation.objects.get(user_id=user_obj.id)
            madrasha_id = user_info.madrasha_id
        except UserInformation.DoesNotExist:
            return None, 'User information not found'

        latest_exam = ExamSetup.objects.order_by('-id').first()
        latest_exam_id = latest_exam.id if latest_exam else None

        markaz_app_data = data.get('markaz_application') or {}
        markaz_app_data['user'] = user_obj.id
        markaz_app_data['madrasa_id'] = madrasha_id
        markaz_app_data['exam'] = latest_exam_id
        markaz_app_serializer = MarkazApplicationSerializer(data=markaz_app_data)
        markaz_app_serializer.is_valid(raise_exception=True)
        markaz_app = markaz_app_serializer.save()

        main_madrasa_info_data = {**data.get('main_madrasa_info', {}), 'markaz_application': markaz_app.id, 'madrasa_id': madrasha_id}
        main_madrasa_serializer = MainMadrasaInfoSerializer(data=main_madrasa_info_data)
        main_madrasa_serializer.is_valid(raise_exception=True)
        main_madrasa_serializer.save()

        associated_madrasas = data.get('associated_madrasas', [])
        for madrasa in associated_madrasas:
            madrasa_data = {**madrasa, 'markaz_application': markaz_app.id}
            # Ensure madrasa_id is properly set from frontend school_id
            if 'madrasa_id' in madrasa_data:
                madrasa_data['madrasa_id'] = madrasa_data['madrasa_id']
            madrasa_serializer = AssociatedMadrasaSerializer(data=madrasa_data)
            madrasa_serializer.is_valid(raise_exception=True)
            madrasa_serializer.save()

        attachments = data.get('attachments', [])
        for attachment in attachments:
            attachment_serializer = AttachmentSerializer(data={**attachment, 'markaz_application': markaz_app.id})
            attachment_serializer.is_valid(raise_exception=True)
            attachment_serializer.save()

    return markaz_app.id, None

def get_schools_by_elhaq(elhaq_query, exact_match=False):
    if not elhaq_query:
        # If no query provided, return empty result
        return []

    # First, find schools by elhaq number
    if exact_match:
        # Exact search - try exact match first, then fall back to partial if no results
        schools = School.objects.filter(elhaqno__iexact=elhaq_query)
        if not schools.exists():
            # If no exact match, try partial search
            schools = School.objects.filter(elhaqno__icontains=elhaq_query)
    else:
        # Partial search (default behavior)
        schools = School.objects.filter(elhaqno__icontains=elhaq_query)

    # Get the school_ids from the found schools
    school_ids = [school.school_id for school in schools]

    # Check which of these school_ids exist in madrasha_centers table
    matching_center_ids = MadrashaCenter.objects.filter(madrasha_id__in=school_ids).values_list('madrasha_id', flat=True)

    # Filter schools to only include those whose school_id matches madrasha_centers.madrasha_id
    filtered_schools = schools.filter(school_id__in=matching_center_ids)

    serializer = SchoolSelectSerializer(filtered_schools, many=True)
    return serializer.data

def madrasa_search_cache(query, exact_match=False):
    redis_client = redis.StrictRedis.from_url(settings.REDIS_URL)

    if not query:
        # If no query provided, return empty result
        return []

    # Get all schools for searching by elhaq
    all_schools_key = "school_table:all"
    cached_all = redis_client.get(all_schools_key)
    if cached_all:
        all_schools = json.loads(cached_all)
    else:
        all_schools = list(School.objects.all().values('id', 'mname', 'elhaqno', 'school_id'))
        redis_client.setex(all_schools_key, 3600, json.dumps(all_schools))

    # First, find schools by elhaq number
    if exact_match:
        # Exact match first, then partial if no results
        exact_matches = [s for s in all_schools if query.lower() == (s['elhaqno'] or '').lower()]
        if exact_matches:
            matched_schools = exact_matches
        else:
            matched_schools = [s for s in all_schools if query.lower() in (s['elhaqno'] or '').lower()]
    else:
        # Partial search (default behavior)
        matched_schools = [s for s in all_schools if query.lower() in (s['elhaqno'] or '').lower()]

    # Get the school_ids from the found schools
    school_ids = [s['school_id'] for s in matched_schools if s['school_id']]

    # Check which of these school_ids exist in madrasha_centers table
    matching_center_ids = MadrashaCenter.objects.filter(madrasha_id__in=school_ids).values_list('madrasha_id', flat=True)

    # Filter schools to only include those whose school_id matches madrasha_centers.madrasha_id
    filtered_schools = [s for s in matched_schools if s['school_id'] in matching_center_ids]

    return filtered_schools[:30]

def get_markaz_applications(user_id):
    r = get_redis_connection()
    if not r:
        # Fallback: return data without caching
        applications = MarkazApplication.objects.filter(user_id=user_id).order_by('-created_at')
        result = []
        for app in applications:
            data = MarkazApplicationSerializer(app).data
            data['formatted_created_at'] = format_bangla_date(app.created_at)
            data['formatted_updated_at'] = format_bangla_date(app.updated_at)
            result.append(data)
        return {"applications": result, "total": len(result)}
    
    cache_key = f"markaz_applications_{user_id}"
    try:
        cached = r.get(cache_key)
        if cached:
            return json.loads(cached)
    except Exception as e:
        print(f"Redis get error: {e}")
    
    applications = MarkazApplication.objects.filter(user_id=user_id).order_by('-created_at')
    result = []
    for app in applications:
        main_madrasa = MainMadrasaInfo.objects.filter(markaz_application_id=app.id).first()
        madrasa_id = main_madrasa.madrasa_id if main_madrasa else None
        madrasa_name = None
        main_total_students = 0
        main_class_counts = {}
        if main_madrasa:
            main_class_counts = {
                'ফযীলত': main_madrasa.fazilat or 0,
                'সানাবিয়া উলইয়া': main_madrasa.sanabiya_ulya or 0,
                'সানাবিয়া': main_madrasa.sanabiya or 0,
                'মুতাওয়াসসিতা': main_madrasa.mutawassita or 0,
                'ইবতেদাইয়্যাহ': main_madrasa.ibtedaiyyah or 0,
                'হিফজুল কোরান': main_madrasa.hifzul_quran or 0,
                'কিরাআত': main_madrasa.qirat or 0,
            }
            main_total_students = sum(main_class_counts.values())
            school = School.objects.filter(school_id=madrasa_id).first()
            madrasa_name = school.mname if school else None

        associated_madrasas = AssociatedMadrasa.objects.filter(markaz_application_id=app.id)
        associated_list = []
        associated_total_students = 0
        associated_class_counts = {
            'ফযীলত': 0,
            'সানাবিয়া উলইয়া': 0,
            'সানাবিয়া': 0,
            'মুতাওয়াসসিতা': 0,
            'ইবতেদাইয়্যাহ': 0,
            'হিফজুল কোরান': 0,
            'কিরাআত': 0,
        }
        for assoc in associated_madrasas:
            assoc_madrasa_id = assoc.madrasa_id
            assoc_madrasa_name = None
            assoc_students = sum([
                assoc.fazilat or 0,
                assoc.sanabiya_ulya or 0,
                assoc.sanabiya or 0,
                assoc.mutawassita or 0,
                assoc.ibtedaiyyah or 0,
                assoc.hifzul_quran or 0,
                assoc.qirat or 0,
            ])
            associated_class_counts['ফযীলত'] += assoc.fazilat or 0
            associated_class_counts['সানাবিয়া উলইয়া'] += assoc.sanabiya_ulya or 0
            associated_class_counts['সানাবিয়া'] += assoc.sanabiya or 0
            associated_class_counts['মুতাওয়াসসিতা'] += assoc.mutawassita or 0
            associated_class_counts['ইবতেদাইয়্যাহ'] += assoc.ibtedaiyyah or 0
            associated_class_counts['হিফজুল কোরান'] += assoc.hifzul_quran or 0
            associated_class_counts['কিরাআত'] += assoc.qirat or 0
            associated_total_students += assoc_students
            if assoc_madrasa_id:
                school = School.objects.filter(school_id=assoc_madrasa_id).first()
                assoc_madrasa_name = school.mname if school else None
            associated_list.append({
                'id': assoc.id,
                'madrasa_id': assoc_madrasa_id,
                'madrasa_name': assoc_madrasa_name,
                'total_students': assoc_students,
            })

        # ---- Exam Name Logic ----
        exam_name = None
        if app.exam_id:
            exam = ExamSetup.objects.filter(id=app.exam_id).first()
            if exam:
                exam_name = exam.exam_name

        result.append({
            'id': app.id,
            'user_id': app.user_id,
            'markaz_type': app.markaz_type,
            'created_at': str(app.created_at),
            'exam_id': app.exam_id,
            'exam_name': exam_name,
            'status': app.status,
            'main_madrasa_id': madrasa_id,
            'main_madrasa_name': madrasa_name,
            'main_total_students': main_total_students,
            'main_class_counts': main_class_counts,
            'associated_madrasas': associated_list,
            'associated_total_students': associated_total_students,
            'associated_class_counts': associated_class_counts,
        })
    
    try:
        r.set(cache_key, json.dumps(result), ex=300)
    except Exception as e:
        print(f"Redis set error: {e}")
    
    return result

def get_markaz_application_detail(pk):
    app = MarkazApplication.objects.get(id=pk)
    main_madrasa = MainMadrasaInfo.objects.filter(markaz_application_id=app.id).first()
    madrasa_id = main_madrasa.madrasa_id if main_madrasa else None
    madrasa_name = None
    main_total_students = 0
    main_class_counts = {}
    if main_madrasa:
        main_class_counts = {
            'ফযীলত': main_madrasa.fazilat or 0,
            'সানাবিয়া উলইয়া': main_madrasa.sanabiya_ulya or 0,
            'সানাবিয়া': main_madrasa.sanabiya or 0,
            'মুতাওয়াসসিতা': main_madrasa.mutawassita or 0,
            'ইবতেদাইয়্যাহ': main_madrasa.ibtedaiyyah or 0,
            'হিফজুল কোরান': main_madrasa.hifzul_quran or 0,
            'কিরাআত': main_madrasa.qirat or 0,
        }
        main_total_students = sum(main_class_counts.values())
        school = School.objects.filter(school_id=madrasa_id).first()
        madrasa_name = school.mname if school else None

    associated_madrasas = AssociatedMadrasa.objects.filter(markaz_application_id=app.id)
    associated_list = []
    associated_total_students = 0
    associated_class_counts = {
        'ফযীলত': 0,
        'সানাবিয়া উলইয়া': 0,
        'সানাবিয়া': 0,
        'মুতাওয়াসসিতা': 0,
        'ইবতেদাইয়্যাহ': 0,
        'হিফজুল কোরান': 0,
        'কিরাআত': 0,
    }
    for assoc in associated_madrasas:
        assoc_madrasa_id = assoc.madrasa_id
        assoc_madrasa_name = None
        assoc_students = sum([
            assoc.fazilat or 0,
            assoc.sanabiya_ulya or 0,
            assoc.sanabiya or 0,
            assoc.mutawassita or 0,
            assoc.ibtedaiyyah or 0,
            assoc.hifzul_quran or 0,
            assoc.qirat or 0,
        ])
        associated_class_counts['ফযীলত'] += assoc.fazilat or 0
        associated_class_counts['সানাবিয়া উলইয়া'] += assoc.sanabiya_ulya or 0
        associated_class_counts['সানাবিয়া'] += assoc.sanabiya or 0
        associated_class_counts['মুতাওয়াসসিতা'] += assoc.mutawassita or 0
        associated_class_counts['ইবতেদাইয়্যাহ'] += assoc.ibtedaiyyah or 0
        associated_class_counts['হিফজুল কোরান'] += assoc.hifzul_quran or 0
        associated_class_counts['কিরাআত'] += assoc.qirat or 0
        associated_total_students += assoc_students
        if assoc_madrasa_id:
            school = School.objects.filter(school_id=assoc_madrasa_id).first()
            assoc_madrasa_name = school.mname if school else None
        associated_list.append({
            'id': assoc.id,
            'madrasa_id': assoc_madrasa_id,
            'madrasa_name': assoc_madrasa_name,
            'total_students': assoc_students,
        })

    # ---- Exam Name Logic ----
    exam_name = None
    if app.exam_id:
        exam = ExamSetup.objects.filter(id=app.exam_id).first()
        if exam:
            exam_name = exam.exam_name

    result = {
        'id': app.id,
        'user_id': app.user_id,
        'markaz_type': app.markaz_type,
        'created_at': str(app.created_at),
        'exam_id': app.exam_id,
        'exam_name': exam_name,
        'status': app.status,
        'main_madrasa_id': madrasa_id,
        'main_madrasa_name': madrasa_name,
        'main_total_students': main_total_students,
        'main_class_counts': main_class_counts,
        'associated_madrasas': associated_list,
        'associated_total_students': associated_total_students,
        'associated_class_counts': associated_class_counts,
    }
    return result

def delete_markaz_application(pk, ip_address):
    app = MarkazApplication.objects.get(id=pk)
    from apps.Markaz.models import MarkazApplicationAudit
    audit = MarkazApplicationAudit.objects.create(
        markaz_application=app,
        action='delete',
        ip_address=ip_address,
        status=app.status,
        printed=app.printed,
        created_at=timezone.now()
    )
    app.delete()
    return True

def edit_markaz_application(pk, request):
    def parse_json_field(field_name):
        field_value = request.data.get(field_name)
        if isinstance(field_value, str):
            try:
                return json.loads(field_value)
            except json.JSONDecodeError:
                return {}
        return field_value or {}

    with transaction.atomic():
        markaz_app_data = parse_json_field('markaz_application')
        main_madrasa_info_data = parse_json_field('main_madrasa_info')
        associated_madrasas_data = parse_json_field('associated_madrasas')
        deleted_madrasa_ids = parse_json_field('deleted_madrasa_ids')
        attachments_data = parse_json_field('attachments')

        markaz_app = MarkazApplication.objects.get(id=pk)
        markaz_app_serializer = MarkazApplicationSerializer(markaz_app, data=markaz_app_data, partial=True)
        markaz_app_serializer.is_valid(raise_exception=True)
        markaz_app_serializer.save()

        # Ensure madrasa_id is automatically populated from user_information for main madrasa
        try:
            user_info = UserInformation.objects.get(user_id=markaz_app.user_id)
            madrasha_id = user_info.madrasha_id
            if madrasha_id and not main_madrasa_info_data.get('madrasa_id'):
                main_madrasa_info_data['madrasa_id'] = madrasha_id
        except UserInformation.DoesNotExist:
            pass

        main_madrasa = MainMadrasaInfo.objects.filter(markaz_application_id=pk).first()
        if main_madrasa:
            main_madrasa_serializer = MainMadrasaInfoSerializer(main_madrasa, data=main_madrasa_info_data, partial=True)
            main_madrasa_serializer.is_valid(raise_exception=True)
            main_madrasa_serializer.save()
        else:
            # Create new main_madrasa_info if it doesn't exist
            main_madrasa_info_data['markaz_application'] = pk
            main_madrasa_serializer = MainMadrasaInfoSerializer(data=main_madrasa_info_data)
            main_madrasa_serializer.is_valid(raise_exception=True)
            main_madrasa_serializer.save()
        for del_id in deleted_madrasa_ids:
            AssociatedMadrasa.objects.filter(id=del_id, markaz_application_id=pk).delete()
        for madrasa_data in associated_madrasas_data:
            assoc_id = madrasa_data.get('id')
            madrasa_data.pop('madrasa_name', None)
            madrasa_data.pop('elhaqno', None)
            if assoc_id:
                assoc_madrasa = AssociatedMadrasa.objects.filter(id=assoc_id, markaz_application_id=pk).first()
                if assoc_madrasa:
                    if f'noc_file_{assoc_id}' in request.FILES:
                        madrasa_data['noc_file_path'] = request.FILES[f'noc_file_{assoc_id}']
                    if f'resolution_file_{assoc_id}' in request.FILES:
                        madrasa_data['resolution_file_path'] = request.FILES[f'resolution_file_{assoc_id}']
                    assoc_madrasa_serializer = AssociatedMadrasaSerializer(assoc_madrasa, data=madrasa_data, partial=True)
                    assoc_madrasa_serializer.is_valid(raise_exception=True)
                    assoc_madrasa_serializer.save()
            else:
                noc_file = madrasa_data.pop('noc_file', None)
                resolution_file = madrasa_data.pop('resolution_file', None)
                new_madrasa = AssociatedMadrasa.objects.create(markaz_application_id=pk, **madrasa_data)
                if noc_file:
                    new_madrasa.noc_file_path = noc_file
                if resolution_file:
                    new_madrasa.resolution_file_path = resolution_file
                new_madrasa.save()
        for attachment_data in attachments_data:
            attach_id = attachment_data.get('id')
            if attach_id:
                attachment = Attachment.objects.filter(id=attach_id, markaz_application_id=pk).first()
                if attachment:
                    attachment_serializer = AttachmentSerializer(attachment, data=attachment_data, partial=True)
                    attachment_serializer.is_valid(raise_exception=True)
                    attachment_serializer.save()
    return True

def get_full_markaz_application(pk):
    markaz_app = MarkazApplication.objects.get(id=pk)
    markaz_app_serializer = MarkazApplicationSerializer(markaz_app)
    main_madrasa_info = MainMadrasaInfo.objects.filter(markaz_application_id=pk).first()
    associated_madrasas = AssociatedMadrasa.objects.filter(markaz_application_id=pk)
    attachments = Attachment.objects.filter(markaz_application_id=pk)
    main_madrasa_info_serializer = MainMadrasaInfoSerializer(main_madrasa_info) if main_madrasa_info else None
    associated_madrasas_serializer = AssociatedMadrasaSerializer(associated_madrasas, many=True)
    attachments_serializer = AttachmentSerializer(attachments, many=True)
    main_class_counts = {}
    if main_madrasa_info:
        main_class_counts = {
            'ফযীলত': main_madrasa_info.fazilat or 0,
            'সানাবিয়া উলইয়া': main_madrasa_info.sanabiya_ulya or 0,
            'সানাবিয়া': main_madrasa_info.sanabiya or 0,
            'মুতাওয়াসসিতা': main_madrasa_info.mutawassita or 0,
            'ইবতেদাইয়্যাহ': main_madrasa_info.ibtedaiyyah or 0,
            'হিফজুল কোরান': main_madrasa_info.hifzul_quran or 0,
            'কিরাআত': main_madrasa_info.qirat or 0,
        }
    associated_class_counts = {
        'ফযীলত': 0,
        'সানাবিয়া উলইয়া': 0,
        'সানাবিয়া': 0,
        'মুতাওয়াসসিতা': 0,
        'ইবতেদাইয়্যাহ': 0,
        'হিফজুল কোরান': 0,
        'কিরাআত': 0,
    }
    for assoc in associated_madrasas:
        associated_class_counts['ফযীলত'] += assoc.fazilat or 0
        associated_class_counts['সানাবিয়া উলইয়া'] += assoc.sanabiya_ulya or 0
        associated_class_counts['সানাবিয়া'] += assoc.sanabiya or 0
        associated_class_counts['মুতাওয়াসসিতা'] += assoc.mutawassita or 0
        associated_class_counts['ইবতেদাইয়্যাহ'] += assoc.ibtedaiyyah or 0
        associated_class_counts['হিফজুল কোরান'] += assoc.hifzul_quran or 0
        associated_class_counts['কিরাআত'] += assoc.qirat or 0

    # ---- Exam Name Logic ----
    exam_name = None
    if markaz_app.exam_id:
        exam = ExamSetup.objects.filter(id=markaz_app.exam_id).first()
        if exam:
            exam_name = exam.exam_name

    response_data = {
        'markaz_application': markaz_app_serializer.data,
        'main_madrasa_info': main_madrasa_info_serializer.data if main_madrasa_info_serializer else {},
        'main_class_counts': main_class_counts,
        'associated_madrasas': associated_madrasas_serializer.data,
        'associated_class_counts': associated_class_counts,
        'attachments': attachments_serializer.data,
        'exam_name': exam_name  # <-- added here as well
    }
    return response_data