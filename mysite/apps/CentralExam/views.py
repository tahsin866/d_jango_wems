from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db import transaction
from django.db.models import Q
from .models import ExamSetup
from .serializers import ExamSetupSerializer


class ExamSetupCreateView(APIView):
    """কেন্দ্রীয় পরীক্ষা সেটআপ তৈরি ভিউ - Laravel store_1 function এর মতো"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        নতুন পরীক্ষা সেটআপ তৈরি করে
        Laravel এর store_1 function এর সমতুল্য
        """
        try:
            # Data validation using serializer
            serializer = ExamSetupSerializer(data=request.data)
            
            if serializer.is_valid():
                # Create exam setup - Laravel এর ExamSetup::create($validated) এর মতো
                exam_setup = serializer.save()
                
                # Return response with status 201 - Laravel এর মতো exact format
                response_data = ExamSetupSerializer(exam_setup).data
                response_data['success'] = True
                response_data['message'] = 'পরীক্ষা সেটআপ সফলভাবে তৈরি হয়েছে'
                
                return Response(
                    response_data,
                    status=status.HTTP_201_CREATED
                )
            else:
                # Validation errors return
                return Response({
                    'success': False,
                    'errors': serializer.errors,
                    'message': 'ডেটা ভ্যালিডেশন ত্রুটি'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                'success': False,
                'errors': {},
                'message': f'পরীক্ষা সেটআপ তৈরিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExamSetupListView(APIView):
    """পরীক্ষা সেটআপ তালিকা ভিউ"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """সব পরীক্ষা সেটআপের তালিকা ফেরত দেয় - Search and Filter support সহ"""
        try:
            # Base queryset
            exam_setups = ExamSetup.objects.all()
            
            # Search filter
            search_query = request.GET.get('search', '').strip()
            if search_query:
                exam_setups = exam_setups.filter(
                    Q(exam_name__icontains=search_query) |
                    Q(arabic_year__icontains=search_query) |
                    Q(bangla_year__icontains=search_query) |
                    Q(english_year__icontains=search_query)
                )
            
            # Year filter
            year_filter = request.GET.get('year', '').strip()
            if year_filter:
                exam_setups = exam_setups.filter(
                    Q(arabic_year=year_filter) |
                    Q(bangla_year=year_filter) |
                    Q(english_year=year_filter)
                )
            
            # Exam name filter
            exam_name_filter = request.GET.get('exam_name', '').strip()
            if exam_name_filter:
                exam_setups = exam_setups.filter(exam_name=exam_name_filter)
            
            # Order by created_at descending
            exam_setups = exam_setups.order_by('-created_at').distinct()
            
            serializer = ExamSetupSerializer(exam_setups, many=True)
            
            # Frontend expects direct array data, not nested in data field
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'data': [],
                'message': f'ডেটা প্রাপ্তিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExamSetupDetailView(APIView):
    """পরীক্ষা সেটআপ বিস্তারিত ভিউ"""
    permission_classes = [AllowAny]
    
    def get(self, request, exam_id):
        """নির্দিষ্ট পরীক্ষা সেটআপের তথ্য ফেরত দেয়"""
        try:
            exam_setup = ExamSetup.objects.get(id=exam_id)
            serializer = ExamSetupSerializer(exam_setup)
            
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'পরীক্ষা সেটআপ তথ্য সফলভাবে প্রাপ্ত হয়েছে'
            }, status=status.HTTP_200_OK)
            
        except ExamSetup.DoesNotExist:
            return Response({
                'success': False,
                'data': {},
                'message': 'পরীক্ষা সেটআপ পাওয়া যায়নি'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'data': {},
                'message': f'ডেটা প্রাপ্তিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExamSetupUpdateView(APIView):
    """পরীক্ষা সেটআপ আপডেট ভিউ"""
    permission_classes = [AllowAny]
    
    def put(self, request, exam_id):
        """পরীক্ষা সেটআপ আপডেট করে"""
        try:
            exam_setup = ExamSetup.objects.get(id=exam_id)
            serializer = ExamSetupSerializer(exam_setup, data=request.data)
            
            if serializer.is_valid():
                exam_setup = serializer.save()
                
                # Return response with success flag
                response_data = ExamSetupSerializer(exam_setup).data
                response_data['success'] = True
                response_data['message'] = 'পরীক্ষা সেটআপ সফলভাবে আপডেট হয়েছে'
                
                return Response(
                    response_data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response({
                    'success': False,
                    'errors': serializer.errors,
                    'message': 'ডেটা ভ্যালিডেশন ত্রুটি'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except ExamSetup.DoesNotExist:
            return Response({
                'success': False,
                'data': {},
                'message': 'পরীক্ষা সেটআপ পাওয়া যায়নি'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'data': {},
                'message': f'পরীক্ষা সেটআপ আপডেটে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExamSetupDeleteView(APIView):
    """পরীক্ষা সেটআপ ডিলিট ভিউ"""
    permission_classes = [AllowAny]
    
    def delete(self, request, exam_id):
        """পরীক্ষা সেটআপ ডিলিট করে"""
        try:
            exam_setup = ExamSetup.objects.get(id=exam_id)
            exam_setup.delete()
            
            return Response({
                'success': True,
                'data': {},
                'message': 'পরীক্ষা সেটআপ সফলভাবে ডিলিট হয়েছে'
            }, status=status.HTTP_200_OK)
            
        except ExamSetup.DoesNotExist:
            return Response({
                'success': False,
                'data': {},
                'message': 'পরীক্ষা সেটআপ পাওয়া যায়নি'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'data': {},
                'message': f'পরীক্ষা সেটআপ ডিলিটে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)