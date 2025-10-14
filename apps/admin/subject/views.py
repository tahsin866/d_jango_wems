from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .service.services import (
    get_marhala_with_counts_service, get_marhala_list_service, get_marhala_subject_list_service,
    create_marhala_subject_service, create_marhala_with_subjects_service, get_marhala_detail_service,
    update_marhala_service, delete_marhala_service, get_subject_settings_list_service,
    create_subject_settings_service, get_subject_settings_detail_service, update_subject_settings_service,
    delete_subject_settings_service, get_subject_data_service, update_subject_setting_service,
    get_exam_fee_list_by_setup_service
)

class MarhalaWithCountsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            data, cached = get_marhala_with_counts_service()
            return Response({
                'success': True,
                'data': data,
                'message': 'মারহালা তালিকা সফলভাবে প্রাপ্ত হয়েছে' + (' (ক্যাশ থেকে)' if cached else ''),
                'cached': cached
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'data': [], 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MarhalaListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            data, cached = get_marhala_list_service()
            return Response({'success': True, 'data': data, 'cached': cached}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'data': [], 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MarhalaSubjectListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            marhala_id = request.query_params.get('marhala_id')
            data = get_marhala_subject_list_service(marhala_id)
            return Response({'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'data': [], 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MarhalaSubjectCreateView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            data = create_marhala_subject_service(request.data)
            return Response({'success': True, 'data': data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'success': False, 'data': {}, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MarhalaWithSubjectsCreateView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        marhala, subjects, missing = create_marhala_with_subjects_service(request.data)
        if missing:
            return Response({'success': False, 'message': f'প্রয়োজনীয় ফিল্ড অনুপস্থিত: {missing}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'success': True,
            'data': {'marhala': marhala, 'subjects': subjects}
        }, status=status.HTTP_201_CREATED)

class MarhalaDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, marhala_id):
        try:
            marhala, subjects = get_marhala_detail_service(marhala_id)
            return Response({
                'success': True,
                'data': {'marhala': marhala, 'subjects': subjects}
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'data': {}, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MarhalaUpdateView(APIView):
    permission_classes = [AllowAny]
    def put(self, request, marhala_id):
        marhala, subjects, missing = update_marhala_service(marhala_id, request.data)
        if missing:
            return Response({'success': False, 'message': f'প্রয়োজনীয় ফিল্ড অনুপস্থিত: {missing}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'success': True,
            'data': {'marhala': marhala, 'subjects': subjects}
        }, status=status.HTTP_200_OK)

class MarhalaDeleteView(APIView):
    permission_classes = [AllowAny]
    def delete(self, request, marhala_id):
        try:
            marhala_name = delete_marhala_service(marhala_id)
            return Response({'success': True, 'data': {}, 'message': f'মারহালা "{marhala_name}" সফলভাবে ডিলিট হয়েছে'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'data': {}, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SubjectSettingsListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        marhala_id = request.query_params.get('marhala_id')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 100))
        try:
            data, pagination, cached = get_subject_settings_list_service(marhala_id, page, page_size)
            return Response({'success': True, 'data': data, 'pagination': pagination, 'cached': cached}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'data': [], 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SubjectSettingsCreateView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            data = create_subject_settings_service(request.data)
            return Response({'success': True, 'data': data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'success': False, 'data': {}, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SubjectSettingsDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, settings_id):
        try:
            data, cached = get_subject_settings_detail_service(settings_id)
            return Response({'success': True, 'data': data, 'cached': cached}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'data': {}, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SubjectSettingsUpdateView(APIView):
    permission_classes = [AllowAny]
    def put(self, request, settings_id):
        try:
            data = update_subject_settings_service(settings_id, request.data)
            return Response({'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'data': {}, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SubjectSettingsDeleteView(APIView):
    permission_classes = [AllowAny]
    def delete(self, request, settings_id):
        try:
            delete_subject_settings_service(settings_id)
            return Response({'success': True, 'data': {}, 'message': 'সাবজেক্ট সেটিংস সফলভাবে ডিলিট হয়েছে'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'data': {}, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetSubjectDataView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, marhala_id):
        try:
            data, cached = get_subject_data_service(marhala_id)
            return Response({'success': True, 'data': data, 'cached': cached}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'data': {}, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateSubjectSettingView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, settings_id):
        result, message = update_subject_setting_service(settings_id, request.data)
        if not result:
            return Response({'success': False, 'message': message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': True, 'message': message}, status=status.HTTP_200_OK)
    def put(self, request, settings_id):
        return self.post(request, settings_id)

class ExamFeeListBySetupView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        exam_setup_id = request.GET.get('exam_setup')
        if not exam_setup_id:
            return Response({'success': False, 'message': 'exam_setup id আবশ্যক'}, status=status.HTTP_400_BAD_REQUEST)
        data, source = get_exam_fee_list_by_setup_service(exam_setup_id)
        if not data:
            return Response({'success': False, 'data': [], 'message': 'কোনো ফি পাওয়া যায়নি'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'data': data, 'source': source}, status=status.HTTP_200_OK)