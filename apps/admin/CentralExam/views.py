# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from . import services
from .serializers import ExamSetupSerializer, ExamFeeSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def exam_setup_list(request):
    data = services.get_exam_setup_list()
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def exam_setup_detail(request, pk):
    data = services.get_exam_setup_detail(pk)
    return Response(data)


class ExamFeeListBySetupView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        exam_setup_id = request.GET.get('exam_setup')
        if not exam_setup_id:
            return Response({'success': False, 'message': 'exam_setup id আবশ্যক'}, status=400)

        fees = services.list_exam_fees_by_setup(exam_setup_id)
        serializer = ExamFeeSerializer(fees, many=True)
        return Response({'success': True, 'data': serializer.data})


class ExamFeeDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, fee_id):
        try:
            exam_fee = services.get_exam_fee_detail(fee_id)
            serializer = ExamFeeSerializer(exam_fee)
            return Response({'success': True, 'data': serializer.data})
        except:
            return Response({'success': False, 'message': 'ফি পাওয়া যায়নি'}, status=404)


class ExamFeeUpdateView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, fee_id):
        updated_fee, errors = services.update_exam_fee(fee_id, request.data)
        if updated_fee:
            return Response({'success': True, 'data': ExamFeeSerializer(updated_fee).data})
        return Response({'success': False, 'errors': errors}, status=400)


class ExamFeeBulkCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        created, errors = services.bulk_create_fees(request.data.get('fees', []))
        if errors and not created:
            return Response({'success': False, 'errors': errors}, status=400)
        return Response({'success': True, 'data': created, 'errors': errors})


class ExamSetupCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        exam_setup, errors = services.create_exam_setup(request.data)
        if exam_setup:
            return Response({'success': True, 'data': ExamSetupSerializer(exam_setup).data}, status=201)
        return Response({'success': False, 'errors': errors}, status=400)


class ExamSetupListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        exam_setups = services.list_exam_setups(
            request.GET.get('search', '').strip(),
            request.GET.get('year', '').strip(),
            request.GET.get('exam_name', '').strip()
        )
        serializer = ExamSetupSerializer(exam_setups, many=True)
        return Response({'success': True, 'data': serializer.data})


class ExamSetupDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, exam_id):
        try:
            exam_setup = services.get_exam_setup(exam_id)
            serializer = ExamSetupSerializer(exam_setup)
            return Response({'success': True, 'data': serializer.data})
        except:
            return Response({'success': False, 'message': 'পরীক্ষা সেটআপ পাওয়া যায়নি'}, status=404)


class ExamSetupUpdateView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, exam_id):
        updated, errors = services.update_exam_setup(exam_id, request.data)
        if updated:
            return Response({'success': True, 'data': ExamSetupSerializer(updated).data})
        return Response({'success': False, 'errors': errors}, status=400)


class ExamSetupDeleteView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, exam_id):
        try:
            services.delete_exam_setup(exam_id)
            return Response({'success': True, 'message': 'ডিলিট সফল'})
        except:
            return Response({'success': False, 'message': 'ডিলিট ব্যর্থ'}, status=404)


class LatestExamSetupAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        latest_exam = services.get_latest_exam_setup()
        if latest_exam:
            return Response({'success': True, 'data': ExamSetupSerializer(latest_exam).data})
        return Response({'success': False, 'message': 'No exam setup found'}, status=404)
