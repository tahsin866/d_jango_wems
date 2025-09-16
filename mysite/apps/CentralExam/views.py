from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.db import transaction
from django.db.models import Q
from mysite.apps.CentralExam.models import ExamFee   # <-- ঠিক path!
from .models import ExamSetup
from .serializers import ExamSetupSerializer, ExamFeeSerializer

class ExamFeeListBySetupView(APIView):
    """একটি পরীক্ষার সব ফি দেখার API (GET)"""
    permission_classes = [AllowAny]

    def get(self, request):
        exam_setup_id = request.GET.get('exam_setup')
        if not exam_setup_id:
            return Response({'success': False, 'message': 'exam_setup id আবশ্যক'}, status=status.HTTP_400_BAD_REQUEST)
        fees = ExamFee.objects.filter(exam_setup_id=exam_setup_id)
        serializer = ExamFeeSerializer(fees, many=True)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)

class ExamFeeDetailView(APIView):
    """একটি ফি ডিটেইল দেখার API (GET)"""
    permission_classes = [AllowAny]

    def get(self, request, fee_id):
        try:
            exam_fee = ExamFee.objects.get(id=fee_id)
            serializer = ExamFeeSerializer(exam_fee)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'ফি তথ্য সফলভাবে প্রাপ্ত হয়েছে'
            }, status=status.HTTP_200_OK)
        except ExamFee.DoesNotExist:
            return Response({
                'success': False,
                'data': {},
                'message': 'ফি পাওয়া যায়নি'
            }, status=status.HTTP_404_NOT_FOUND)

class ExamFeeUpdateView(APIView):
    """একটি ফি আপডেট করার API (PUT/PATCH)"""
    permission_classes = [AllowAny]

    def put(self, request, fee_id):
        try:
            exam_fee = ExamFee.objects.get(id=fee_id)
        except ExamFee.DoesNotExist:
            return Response(
                {'success': False, 'message': 'ফি আইডি পাওয়া যায়নি'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ExamFeeSerializer(exam_fee, data=request.data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():
                updated_fee = serializer.save()
            return Response(
                {
                    'success': True,
                    'data': ExamFeeSerializer(updated_fee).data,
                    'message': 'ফি সফলভাবে আপডেট হয়েছে'
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'success': False,
                'errors': serializer.errors,
                'message': 'ডেটা ভ্যালিডেশন ত্রুটি'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class ExamFeeBulkCreateView(APIView):
    """একাধিক ফি ইনসার্ট করার API (bulk insert)"""
    permission_classes = [AllowAny]

    def post(self, request):
        fees = request.data.get('fees')
        if not fees or not isinstance(fees, list):
            return Response(
                {'success': False, 'message': 'fees ফিল্ডটি আবশ্যক এবং array হতে হবে'},
                status=status.HTTP_400_BAD_REQUEST
            )
        errors = []
        created_fees = []
        with transaction.atomic():
            for fee in fees:
                serializer = ExamFeeSerializer(data=fee)
                if serializer.is_valid():
                    created_fee = serializer.save()
                    created_fees.append(ExamFeeSerializer(created_fee).data)
                else:
                    errors.append(serializer.errors)
        if errors:
            return Response(
                {'success': False, 'errors': errors, 'message': 'কিছু ফি ইনসার্ট হয়নি'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'success': True, 'data': created_fees, 'message': 'সব ফি সফলভাবে সংরক্ষণ হয়েছে'},
            status=status.HTTP_201_CREATED
        )

class ExamSetupCreateView(APIView):
    """কেন্দ্রীয় পরীক্ষা সেটআপ তৈরি ভিউ"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ExamSetupSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                exam_setup = serializer.save()
            response_data = ExamSetupSerializer(exam_setup).data
            response_data['success'] = True
            response_data['message'] = 'পরীক্ষা সেটআপ সফলভাবে তৈরি হয়েছে'
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(
            {
                'success': False,
                'errors': serializer.errors,
                'message': 'ডেটা ভ্যালিডেশন ত্রুটি'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class ExamSetupListView(APIView):
    """পরীক্ষা সেটআপ তালিকা ভিউ"""
    permission_classes = [AllowAny]

    def get(self, request):
        exam_setups = ExamSetup.objects.all()
        search_query = request.GET.get('search', '').strip()
        if search_query:
            exam_setups = exam_setups.filter(
                Q(exam_name__icontains=search_query) |
                Q(arabic_year__icontains=search_query) |
                Q(bangla_year__icontains=search_query) |
                Q(english_year__icontains=search_query)
            )
        year_filter = request.GET.get('year', '').strip()
        if year_filter:
            exam_setups = exam_setups.filter(
                Q(arabic_year=year_filter) |
                Q(bangla_year=year_filter) |
                Q(english_year=year_filter)
            )
        exam_name_filter = request.GET.get('exam_name', '').strip()
        if exam_name_filter:
            exam_setups = exam_setups.filter(exam_name=exam_name_filter)
        exam_setups = exam_setups.order_by('-created_at').distinct()
        serializer = ExamSetupSerializer(exam_setups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExamSetupDetailView(APIView):
    """পরীক্ষা সেটআপ বিস্তারিত ভিউ"""
    permission_classes = [AllowAny]

    def get(self, request, exam_id):
        try:
            exam_setup = ExamSetup.objects.get(id=exam_id)
            serializer = ExamSetupSerializer(exam_setup)
            return Response(
                {
                    'success': True,
                    'data': serializer.data,
                    'message': 'পরীক্ষা সেটআপ তথ্য সফলভাবে প্রাপ্ত হয়েছে'
                },
                status=status.HTTP_200_OK
            )
        except ExamSetup.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'data': {},
                    'message': 'পরীক্ষা সেটআপ পাওয়া যায়নি'
                },
                status=status.HTTP_404_NOT_FOUND
            )

class ExamSetupUpdateView(APIView):
    """পরীক্ষা সেটআপ আপডেট ভিউ"""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def put(self, request, exam_id):
        try:
            exam_setup = ExamSetup.objects.get(id=exam_id)
        except ExamSetup.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'data': {},
                    'message': 'পরীক্ষা সেটআপ পাওয়া যায়নি'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ExamSetupSerializer(exam_setup, data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                exam_setup = serializer.save()
            response_data = ExamSetupSerializer(exam_setup).data
            response_data['success'] = True
            response_data['message'] = 'পরীক্ষা সেটআপ সফলভাবে আপডেট হয়েছে'
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(
            {
                'success': False,
                'errors': serializer.errors,
                'message': 'ডেটা ভ্যালিডেশন ত্রুটি'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class ExamSetupDeleteView(APIView):
    """পরীক্ষা সেটআপ ডিলিট ভিউ"""
    permission_classes = [AllowAny]

    def delete(self, request, exam_id):
        try:
            exam_setup = ExamSetup.objects.get(id=exam_id)
        except ExamSetup.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'data': {},
                    'message': 'পরীক্ষা সেটআপ পাওয়া যায়নি'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        with transaction.atomic():
            exam_setup.delete()
        return Response(
            {
                'success': True,
                'data': {},
                'message': 'পরীক্ষা সেটআপ সফলভাবে ডিলিট হয়েছে'
            },
            status=status.HTTP_200_OK
        )