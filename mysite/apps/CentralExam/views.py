from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.db import transaction
from django.db.models import Q
from mysite.apps.CentralExam.models import ExamFee   # <-- ঠিক path!
from .models import ExamSetup
from .serializers import ExamSetupSerializer, ExamFeeSerializer
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.core.cache import cache
import json

from .models import ExamSetup
from .serializers import ExamSetupSerializer






@api_view(['GET'])
@permission_classes([AllowAny])
def exam_setup_list(request):
    cache_key = "exam_setup_list"
    data = cache.get(cache_key)

    if data is None:  # প্রথমবার DB থেকে লোড
        exam_setups = ExamSetup.objects.all()
        serializer = ExamSetupSerializer(exam_setups, many=True)
        data = serializer.data
        cache.set(cache_key, json.dumps(data), timeout=60*30)  # ৩০ মিনিট ক্যাশ
    else:
        data = json.loads(data)

    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def exam_setup_detail(request, pk):
    cache_key = f"exam_setup_{pk}"
    data = cache.get(cache_key)

    if data is None:  # প্রথমবার DB থেকে লোড
        exam_setup = get_object_or_404(ExamSetup, pk=pk)
        serializer = ExamSetupSerializer(exam_setup)
        data = serializer.data
        cache.set(cache_key, json.dumps(data), timeout=60*30)  # ৩০ মিনিট ক্যাশ
    else:
        data = json.loads(data)

    return Response(data)









# Consistent response structure helper (function-style comment only; no new imports)
# response shape used everywhere:
# {
#   "success": bool,
#   "data": ... (object/array) or {},
#   "errors": ... (object/array) or [],
#   "message": "..."
# }

class ExamFeeListBySetupView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            exam_setup_id = request.GET.get('exam_setup')
            if not exam_setup_id:
                return Response({
                    'success': False,
                    'data': {},
                    'errors': {'exam_setup': ['exam_setup id আবশ্যক']},
                    'message': 'exam_setup id আবশ্যক'
                }, status=status.HTTP_400_BAD_REQUEST)

            # performance: select_related for fk relations used in serializer/display
            fees = ExamFee.objects.filter(exam_setup_id=exam_setup_id).select_related('marhala', 'exam_setup')
            serializer = ExamFeeSerializer(fees, many=True)
            return Response({
                'success': True,
                'data': serializer.data,
                'errors': [],
                'message': 'ফি তালিকা প্রাপ্ত হয়েছে'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'data': {},
                'errors': {'detail': [str(e)]},
                'message': 'সার্ভার এরর'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ExamFeeDetailView(APIView):
    """একটি ফি ডিটেইল দেখার API (GET)"""
    permission_classes = [AllowAny]

    def get(self, request, fee_id):
        try:
            exam_fee = ExamFee.objects.select_related('marhala', 'exam_setup').get(id=fee_id)
            serializer = ExamFeeSerializer(exam_fee)
            return Response({
                'success': True,
                'data': serializer.data,
                'errors': [],
                'message': 'ফি তথ্য সফলভাবে প্রাপ্ত হয়েছে'
            }, status=status.HTTP_200_OK)
        except ExamFee.DoesNotExist:
            return Response({
                'success': False,
                'data': {},
                'errors': {'id': ['ফি পাওয়া যায়নি']},
                'message': 'ফি পাওয়া যায়নি'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'data': {},
                'errors': {'detail': [str(e)]},
                'message': 'সার্ভার এরর'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ExamFeeUpdateView(APIView):
    """একটি ফি আপডেট করার API (PUT/PATCH)"""
    permission_classes = [AllowAny]

    def put(self, request, fee_id):
        try:
            exam_fee = ExamFee.objects.get(id=fee_id)
        except ExamFee.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'data': {},
                    'errors': {'id': ['ফি আইডি পাওয়া যায়নি']},
                    'message': 'ফি আইডি পাওয়া যায়নি'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # production-ready: allow partial updates so client doesn't need to send all fields
        serializer = ExamFeeSerializer(exam_fee, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    updated_fee = serializer.save()
                return Response(
                    {
                        'success': True,
                        'data': ExamFeeSerializer(updated_fee).data,
                        'errors': [],
                        'message': 'ফি সফলভাবে আপডেট হয়েছে'
                    },
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response({
                    'success': False,
                    'data': {},
                    'errors': {'detail': [str(e)]},
                    'message': 'সার্ভার এরর'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {
                'success': False,
                'data': {},
                'errors': serializer.errors,
                'message': 'ডেটা ভ্যালিডেশন ত্রুটি'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

# views.py - SIMPLIFIED BULK CREATE VIEW

class ExamFeeBulkCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            fees = request.data.get('fees')
            if not fees or not isinstance(fees, list):
                return Response({
                    'success': False,
                    'data': {},
                    'errors': {'fees': ['fees ফিল্ডটি আবশ্যক এবং array হতে হবে']},
                    'message': 'fees ফিল্ডটি আবশ্যক এবং array হতে হবে'
                }, status=status.HTTP_400_BAD_REQUEST)

            created_fees = []
            errors = []

            # Check if any exam_setup exists before loop
            latest_exam = ExamSetup.objects.order_by('-id').first()
            if not latest_exam:
                return Response({
                    'success': False,
                    'data': [],
                    'errors': [{'exam_setup': ['কোনো কেন্দ্রীয় পরীক্ষা পাওয়া যায়নি']}],
                    'message': 'কোনো কেন্দ্রীয় পরীক্ষা পাওয়া যায়নি',
                    'summary': {
                        'total_items': len(fees),
                        'successful': 0,
                        'failed': len(fees)
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

            for idx, fee_data in enumerate(fees):
                print(f"[DEBUG] Processing fee {idx}: {fee_data}")
                # Auto set latest exam_setup id if missing
                if not fee_data.get('exam_setup'):
                    fee_data['exam_setup'] = latest_exam.id

                # ✅ Direct serializer validation - কোন manipulation নেই
                serializer = ExamFeeSerializer(data=fee_data)
                if not serializer.is_valid():
                    print(f"[DEBUG] Serializer validation failed: {serializer.errors}")
                    errors.append({
                        'index': idx, 
                        'errors': serializer.errors,
                        'item_data': fee_data
                    })
                    continue

                # ✅ Database save
                try:
                    with transaction.atomic():
                        created_fee = serializer.save()
                        created_fees.append(ExamFeeSerializer(created_fee).data)
                        print(f"[DEBUG] Successfully saved fee {idx}")
                except Exception as save_error:
                    print(f"[DEBUG] Save error for fee {idx}: {save_error}")
                    errors.append({
                        'index': idx, 
                        'errors': {'database_error': [str(save_error)]},
                        'item_data': fee_data
                    })

            # ✅ Response handling
            if errors and not created_fees:
                return Response({
                    'success': False,
                    'data': [],
                    'errors': errors,
                    'message': f'কোনো ফি সংরক্ষণ হয়নি - {len(errors)}টি সমস্যা পাওয়া গেছে',
                    'summary': {
                        'total_items': len(fees),
                        'successful': 0,
                        'failed': len(errors)
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

            if errors and created_fees:
                return Response({
                    'success': False,  # Partial success = False
                    'data': created_fees,
                    'errors': errors,
                    'message': f'{len(created_fees)}টি সফল, {len(errors)}টি ব্যর্থ',
                    'summary': {
                        'total_items': len(fees),
                        'successful': len(created_fees),
                        'failed': len(errors)
                    }
                }, status=status.HTTP_207_MULTI_STATUS)

            return Response({
                'success': True,
                'data': created_fees,
                'errors': [],
                'message': f'সব {len(created_fees)}টি ফি সফলভাবে সংরক্ষণ হয়েছে',
                'summary': {
                    'total_items': len(fees),
                    'successful': len(created_fees),
                    'failed': 0
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"[ERROR] Unexpected error in bulk create: {str(e)}")
            import traceback
            traceback.print_exc()
            
            return Response({
                'success': False,
                'data': {},
                'errors': {'server_error': [str(e)]},
                'message': f'সার্ভার এরর: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExamSetupCreateView(APIView):
    """কেন্দ্রীয় পরীক্ষা সেটআপ তৈরি ভিউ"""
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = ExamSetupSerializer(data=request.data)
            if serializer.is_valid():
                with transaction.atomic():
                    exam_setup = serializer.save()
                response_data = ExamSetupSerializer(exam_setup).data
                return Response({
                    'success': True,
                    'data': response_data,
                    'errors': [],
                    'message': 'পরীক্ষা সেটআপ সফলভাবে তৈরি হয়েছে'
                }, status=status.HTTP_201_CREATED)

            return Response(
                {
                    'success': False,
                    'data': {},
                    'errors': serializer.errors,
                    'message': 'ডেটা ভ্যালিডেশন ত্রুটি'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response({
                'success': False,
                'data': {},
                'errors': {'detail': [str(e)]},
                'message': 'সার্ভার এরর'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ExamSetupListView(APIView):
    """পরীক্ষা সেটআপ তালিকা ভিউ"""
    permission_classes = [AllowAny]

    def get(self, request):
        try:
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

            exam_setups = exam_setups.order_by('-created_at')
            serializer = ExamSetupSerializer(exam_setups, many=True)
            return Response({
                'success': True,
                'data': serializer.data,
                'errors': [],
                'message': 'পরীক্ষা সেটআপ তালিকা সফলভাবে প্রাপ্ত হয়েছে'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'data': {},
                'errors': {'detail': [str(e)]},
                'message': 'সার্ভার এরর'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                    'errors': [],
                    'message': 'পরীক্ষা সেটআপ তথ্য সফলভাবে প্রাপ্ত হয়েছে'
                },
                status=status.HTTP_200_OK
            )
        except ExamSetup.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'data': {},
                    'errors': {'id': ['পরীক্ষা সেটআপ পাওয়া যায়নি']},
                    'message': 'পরীক্ষা সেটআপ পাওয়া যায়নি'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({
                'success': False,
                'data': {},
                'errors': {'detail': [str(e)]},
                'message': 'সার্ভার এরর'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ExamSetupUpdateView(APIView):
    """পরীক্ষা সেটআপ আপডেট ভিউ"""
    permission_classes = [AllowAny]

    def put(self, request, exam_id):
        try:
            exam_setup = ExamSetup.objects.get(id=exam_id)
        except ExamSetup.DoesNotExist:
            return Response(
                {
                    'success': False,
                    'data': {},
                    'errors': {'id': ['পরীক্ষা সেটআপ পাওয়া যায়নি']},
                    'message': 'পরীক্ষা সেটআপ পাওয়া যায়নি'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # allow partial updates so client can send only changed fields
        serializer = ExamSetupSerializer(exam_setup, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    exam_setup = serializer.save()
                response_data = ExamSetupSerializer(exam_setup).data
                return Response({
                    'success': True,
                    'data': response_data,
                    'errors': [],
                    'message': 'পরীক্ষা সেটআপ সফলভাবে আপডেট হয়েছে'
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    'success': False,
                    'data': {},
                    'errors': {'detail': [str(e)]},
                    'message': 'সার্ভার এরর'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {
                'success': False,
                'data': {},
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
                    'errors': {'id': ['পরীক্ষা সেটআপ পাওয়া যায়নি']},
                    'message': 'পরীক্ষা সেটআপ পাওয়া যায়নি'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            with transaction.atomic():
                exam_setup.delete()
            return Response(
                {
                    'success': True,
                    'data': {},
                    'errors': [],
                    'message': 'পরীক্ষা সেটআপ সফলভাবে ডিলিট হয়েছে'
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({
                'success': False,
                'data': {},
                'errors': {'detail': [str(e)]},
                'message': 'সার্ভার এরর'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LatestExamSetupAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        
        latest_exam = ExamSetup.objects.order_by('-id').first()
        if latest_exam:
            data = ExamSetupSerializer(latest_exam).data
            return Response({'success': True, 'data': data, 'errors': [], 'message': 'Latest exam setup found.'})
        return Response({'success': False, 'data': {}, 'errors': ['No exam setup found.'], 'message': 'No exam setup found.'}, status=404)