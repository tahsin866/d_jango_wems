import redis
from django.conf import settings
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mysite.apps.school.models import School
from mysite.apps.Markaz.serializers import SchoolSelectSerializer, MarkazApplicationSerializer, MainMadrasaInfoSerializer, AssociatedMadrasaSerializer, AttachmentSerializer
from .models import MarkazApplication, MainMadrasaInfo, AssociatedMadrasa, Attachment
from django.db import transaction
from rest_framework.permissions import AllowAny, IsAuthenticated

class MarkazApplicationCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        # Check user type
        if not hasattr(user, 'user_type') or str(user.user_type.name).lower() != 'madrasha':
            return Response({'success': False, 'error': 'Only madrasha users can insert data.'}, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        try:
            with transaction.atomic():
                # Create MarkazApplication with actual user id
                markaz_app_data = data.get('markaz_application') or {}
                markaz_app_data['user'] = user.id
                markaz_app_serializer = MarkazApplicationSerializer(data=markaz_app_data)
                markaz_app_serializer.is_valid(raise_exception=True)
                markaz_app = markaz_app_serializer.save()

                # Create MainMadrasaInfo
                main_madrasa_serializer = MainMadrasaInfoSerializer(data={**data.get('main_madrasa_info', {}), 'markaz_application': markaz_app.id})
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
        query = request.GET.get('elhaq', '').strip()
        cache_key = f"school_search:{query}"

        # Redis connection (assumes settings.REDIS_URL is set)
        redis_client = redis.StrictRedis.from_url(settings.REDIS_URL)

        # Try Redis cache first
        cached = redis_client.get(cache_key)
        if cached:
            import json
            return Response(json.loads(cached))

        # Exact match search
        if query:
            queryset = School.objects.filter(elhaqno__iexact=query)
        else:
            queryset = School.objects.all()[:30]

        serializer = SchoolSelectSerializer(queryset, many=True)
        data = serializer.data

        # Save to Redis cache (expire in 1 hour)
        import json
        redis_client.setex(cache_key, 3600, json.dumps(data))

        return Response(data)
