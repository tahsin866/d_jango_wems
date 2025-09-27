import redis
from django.conf import settings
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mysite.apps.school.models import School
from mysite.apps.Markaz.serializers import SchoolSelectSerializer, MarkazApplicationSerializer, MainMadrasaInfoSerializer, AssociatedMadrasaSerializer, AttachmentSerializer
from .models import MarkazApplication, MainMadrasaInfo, AssociatedMadrasa, Attachment
from django.db import transaction, connection
from rest_framework.permissions import AllowAny

class MarkazApplicationCreateView(APIView):
   
    permission_classes = [AllowAny]
    def post(self, request):
        # --- Debug: Print all possible header sources ---
        print("[Markaz Debug] Authorization header:", request.headers.get('Authorization'))
        print("[Markaz Debug] META HTTP_AUTHORIZATION:", request.META.get('HTTP_AUTHORIZATION'))
        # --- Extract session_token from all possible sources ---
        session_token = (
            request.headers.get('Authorization') or
            request.META.get('HTTP_AUTHORIZATION') or
            ''
        ).replace('Bearer ', '')
        print("[Markaz Debug] Extracted session_token:", session_token)
        from mysite.apps.users.models import UserSessions, User
        user_id = None
        user_obj = None
        if session_token:
            from django.utils import timezone
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT user_id, expires_at FROM user_sessions WHERE session_token = %s AND is_active = TRUE
                """, [session_token])
                row = cursor.fetchone()
                print("[Markaz Debug] DB session row:", row)
                if row:
                    user_id, expires_at = row
                    from django.utils.timezone import is_aware, make_aware
                    now = timezone.now()
                    # Ensure both datetimes are aware
                    if expires_at:
                        if not is_aware(expires_at):
                            expires_at = make_aware(expires_at)
                        if not is_aware(now):
                            now = make_aware(now)
                        if expires_at < now:
                            print("[Markaz Debug] Session expired.")
                            return Response({'success': False, 'error': 'Session expired.'}, status=status.HTTP_401_UNAUTHORIZED)
                    try:
                        user_obj = User.objects.get(id=user_id)
                        print("[Markaz Debug] User found:", user_obj.id)
                    except User.DoesNotExist:
                        print("[Markaz Debug] User not found for id:", user_id)
                        return Response({'success': False, 'error': 'User not found.'}, status=status.HTTP_401_UNAUTHORIZED)
        if not user_obj:
            print("[Markaz Debug] No user_obj, authentication failed.")
            return Response({'success': False, 'error': 'Authentication credentials were not provided.'}, status=status.HTTP_403_FORBIDDEN)

        # Check user type (case-insensitive, handle None)
        user_type_name = getattr(getattr(user_obj, 'user_type', None), 'name', None)
        if not user_type_name or user_type_name.strip().lower() != 'madrasha':
            return Response({'success': False, 'error': 'Only madrasha users can insert data.'}, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        try:
            from mysite.apps.users.models import UserInformation
            with transaction.atomic():
                # Get madrasa_id from user_information table
                madrasha_id = None
                try:
                    user_info = UserInformation.objects.get(user_id=user_obj.id)
                    madrasha_id = user_info.madrasha_id
                except UserInformation.DoesNotExist:
                    return Response({'success': False, 'error': 'User information not found.'}, status=status.HTTP_400_BAD_REQUEST)

                # Get latest exam id from exam_setups table
                from mysite.apps.CentralExam.models import ExamSetup
                latest_exam = ExamSetup.objects.order_by('-id').first()
                latest_exam_id = latest_exam.id if latest_exam else None

                # Create MarkazApplication with actual user id, madrasa_id, and latest exam id
                markaz_app_data = data.get('markaz_application') or {}
                markaz_app_data['user'] = user_obj.id
                markaz_app_data['madrasa_id'] = madrasha_id
                markaz_app_data['exam'] = latest_exam_id
                markaz_app_serializer = MarkazApplicationSerializer(data=markaz_app_data)
                markaz_app_serializer.is_valid(raise_exception=True)
                markaz_app = markaz_app_serializer.save()

                # Create MainMadrasaInfo
                main_madrasa_info_data = {**data.get('main_madrasa_info', {}), 'markaz_application': markaz_app.id, 'madrasa': madrasha_id}
                main_madrasa_serializer = MainMadrasaInfoSerializer(data=main_madrasa_info_data)
                main_madrasa_serializer.is_valid(raise_exception=True)
                main_madrasa_serializer.save()

                # Create AssociatedMadrasas
                associated_madrasas = data.get('associated_madrasas', [])
                for madrasa in associated_madrasas:
                    madrasa_serializer = AssociatedMadrasaSerializer(data={**madrasa, 'markaz_application': markaz_app.id})
                    madrasa_serializer.is_valid(raise_exception=True)
                    madrasa_serializer.save()

                # Create Attachments
                attachments = data.get('attachments', [])
                for attachment in attachments:
                    attachment_serializer = AttachmentSerializer(data={**attachment, 'markaz_application': markaz_app.id})
                    attachment_serializer.is_valid(raise_exception=True)
                    attachment_serializer.save()

            return Response({'success': True, 'markaz_application_id': markaz_app.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.permissions import AllowAny

class MadrashaSelectByElhaq(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        elhaq_query = request.GET.get('elhaq', '').strip()
        if not elhaq_query:
            schools = School.objects.all()[:30]  # প্রথম ৩০টা দেখান
        else:
            schools = School.objects.filter(elhaqno__icontains=elhaq_query)
        serializer = SchoolSelectSerializer(schools, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MadrasaSearchAPIView(APIView):
    def get(self, request):
        import json
        query = request.GET.get('elhaq', '').strip()
        redis_client = redis.StrictRedis.from_url(settings.REDIS_URL)
        # Cache key for all schools
        all_schools_key = "school_table:all"
        # Try to load all schools from Redis
        cached_all = redis_client.get(all_schools_key)
        if cached_all:
            all_schools = json.loads(cached_all)
        else:
            all_schools = list(School.objects.all().values('id', 'mname', 'elhaqno'))
            redis_client.setex(all_schools_key, 3600, json.dumps(all_schools))
        # Filter by elhaq query (case-insensitive contains)
        if query:
            filtered = [s for s in all_schools if query.lower() in (s['elhaqno'] or '').lower()]
        else:
            filtered = all_schools[:30]
        return Response(filtered)
