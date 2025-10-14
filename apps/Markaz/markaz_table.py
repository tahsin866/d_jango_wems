from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone
import pytz

from apps.Markaz.models import MarkazApplication, MainMadrasaInfo, AssociatedMadrasa
from apps.school.models import School
from apps.admin.CentralExam.models import ExamSetup
from apps.Markaz.service import get_redis_connection

BN_MONTHS = [
    'জানুয়ারি', 'ফেব্রুয়ারি', 'মার্চ', 'এপ্রিল', 'মে', 'জুন',
    'জুলাই', 'আগস্ট', 'সেপ্টেম্বর', 'অক্টোবর', 'নভেম্বর', 'ডিসেম্বর'
]

def format_bangla_date(dt):
    if not dt:
        return ''
    dt = dt.astimezone(pytz.timezone('Asia/Dhaka'))
    return f"{dt.day} {BN_MONTHS[dt.month - 1]}, {dt.year}"

class MarkazApplicationListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        import json
        user_id = request.user.id
        cache_key = f"markaz_applications_{user_id}"
        r = get_redis_connection()
        
        cached = None
        if r:
            try:
                cached = r.get(cache_key)
            except Exception as e:
                print(f"Redis get error: {e}")
        
        if cached:
            result = json.loads(cached)
            print("Loaded from Redis cache")
        else:
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
                    school = School.objects.filter(id=madrasa_id).first()
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
                    # Per-class count
                    associated_class_counts['ফযীলত'] += assoc.fazilat or 0
                    associated_class_counts['সানাবিয়া উলইয়া'] += assoc.sanabiya_ulya or 0
                    associated_class_counts['সানাবিয়া'] += assoc.sanabiya or 0
                    associated_class_counts['মুতাওয়াসসিতা'] += assoc.mutawassita or 0
                    associated_class_counts['ইবতেদাইয়্যাহ'] += assoc.ibtedaiyyah or 0
                    associated_class_counts['হিফজুল কোরান'] += assoc.hifzul_quran or 0
                    associated_class_counts['কিরাআত'] += assoc.qirat or 0
                    associated_total_students += assoc_students
                    if assoc_madrasa_id:
                        school = School.objects.filter(id=assoc_madrasa_id).first()
                        assoc_madrasa_name = school.mname if school else None
                    associated_list.append({
                        'id': assoc.id,
                        'madrasa_id': assoc_madrasa_id,
                        'madrasa_name': assoc_madrasa_name,
                        'total_students': assoc_students,
                    })

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
            
            if r:
                try:
                    r.set(cache_key, json.dumps(result), ex=300)  # Cache for 5 minutes
                    print("Loaded from DB and cached in Redis")
                except Exception as e:
                    print(f"Redis set error: {e}")
                    print("Loaded from DB (Redis cache failed)")
            else:
                print("Loaded from DB (Redis not available)")
        
        return Response({'success': True, 'data': result}, status=status.HTTP_200_OK)

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class MarkazApplicationDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk=None):
        if pk is None:
            return Response({'success': False, 'error': 'No ID provided.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            app = MarkazApplication.objects.get(id=pk)
            # Main MadrasaInfo fetch, Associated Madrasa fetch, Exam fetch (code same as above, just for one app)
            # ... (copy code from above for one instance)
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
                school = School.objects.filter(id=madrasa_id).first()
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
                # Per-class count
                associated_class_counts['ফযীলত'] += assoc.fazilat or 0
                associated_class_counts['সানাবিয়া উলইয়া'] += assoc.sanabiya_ulya or 0
                associated_class_counts['সানাবিয়া'] += assoc.sanabiya or 0
                associated_class_counts['মুতাওয়াসসিতা'] += assoc.mutawassita or 0
                associated_class_counts['ইবতেদাইয়্যাহ'] += assoc.ibtedaiyyah or 0
                associated_class_counts['হিফজুল কোরান'] += assoc.hifzul_quran or 0
                associated_class_counts['কিরাআত'] += assoc.qirat or 0
                associated_total_students += assoc_students
                if assoc_madrasa_id:
                    school = School.objects.filter(id=assoc_madrasa_id).first()
                    assoc_madrasa_name = school.mname if school else None
                associated_list.append({
                    'id': assoc.id,
                    'madrasa_id': assoc_madrasa_id,
                    'madrasa_name': assoc_madrasa_name,
                    'total_students': assoc_students,
                })

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
            return Response({'success': True, 'data': result}, status=status.HTTP_200_OK)
        except MarkazApplication.DoesNotExist:
            return Response({'success': False, 'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk=None):
        if pk is None:
            return Response({'success': False, 'error': 'No ID provided.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            app = MarkazApplication.objects.get(id=pk)
            # Audit entry
            from apps.Markaz.models import MarkazApplicationAudit
            audit = MarkazApplicationAudit.objects.create(
                markaz_application=app,
                action='delete',
                ip_address=request.META.get('REMOTE_ADDR'),
                status=app.status,
                printed=app.printed,
                created_at=timezone.now()
            )
            print('Audit entry created:', audit.id, audit.action, audit.ip_address)
            app.delete()
            return Response({'success': True, 'message': 'Deleted successfully.'}, status=status.HTTP_200_OK)
        except MarkazApplication.DoesNotExist:
            return Response({'success': False, 'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            import traceback
            print('Delete error:', str(e))
            traceback.print_exc()
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)