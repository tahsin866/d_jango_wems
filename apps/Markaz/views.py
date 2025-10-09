from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .service import (
    extract_user_from_token, check_madrasha_user, create_markaz_application,
    get_schools_by_elhaq, madrasa_search_cache, get_markaz_applications,
    get_markaz_application_detail, delete_markaz_application,
    edit_markaz_application, get_full_markaz_application
)

class MarkazApplicationCreateView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user_obj, error = extract_user_from_token(request)
        if error:
            return Response({'success': False, 'error': error}, status=status.HTTP_401_UNAUTHORIZED)
        if not user_obj or not check_madrasha_user(user_obj):
            return Response({'success': False, 'error': 'Only madrasha users can insert data.'}, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        application_id, error = create_markaz_application(data, user_obj)
        if error:
            return Response({'success': False, 'error': error}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': True, 'markaz_application_id': application_id}, status=status.HTTP_201_CREATED)

class MadrashaSelectByElhaq(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        elhaq_query = request.GET.get('elhaq', '').strip()
        exact_match = request.GET.get('exact', 'false').lower() == 'true'
        schools_data = get_schools_by_elhaq(elhaq_query, exact_match)
        return Response(schools_data, status=status.HTTP_200_OK)

class MadrasaSearchAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        query = request.GET.get('elhaq', '').strip()
        exact_match = request.GET.get('exact', 'false').lower() == 'true'
        filtered = madrasa_search_cache(query, exact_match)
        return Response(filtered, status=status.HTTP_200_OK)

class MarkazApplicationListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        user_id = request.user.id
        result = get_markaz_applications(user_id)
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
            result = get_markaz_application_detail(pk)
            return Response({'success': True, 'data': result}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'success': False, 'error': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk=None):
        if pk is None:
            return Response({'success': False, 'error': 'No ID provided.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            ip_address = request.META.get('REMOTE_ADDR')
            delete_markaz_application(pk, ip_address)
            return Response({'success': True, 'message': 'Deleted successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MarkazApplicationEditView(APIView):
    permission_classes = [AllowAny]
    def put(self, request, pk=None):
        if pk is None:
            return Response({'success': False, 'error': 'No ID provided.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            edit_markaz_application(pk, request)
            return Response({'success': True, 'message': 'Updated successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MarkazApplicationFullDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk=None):
        if pk is None:
            return Response({'success': False, 'error': 'No ID provided.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            response_data = get_full_markaz_application(pk)
            return Response({'success': True, 'data': response_data}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'success': False, 'error': 'MarkazApplication not found.'}, status=status.HTTP_404_NOT_FOUND)