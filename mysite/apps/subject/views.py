from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Count, Q
from django.db import transaction
from django.conf import settings
from .models import Marhala, MarhalaSubject, SubjectSettings
from mysite.apps.CentralExam.models import ExamFee
from mysite.apps.CentralExam.models import ExamFee
from .serializers import (
    MarhalaWithCountsSerializer, MarhalaSerializer,
    MarhalaSubjectSerializer, SubjectSettingsSerializer
)
from mysite.apps.CentralExam.serializers import ExamFeeSerializer
from .cache import SubjectCache

# ====== Utility Functions ======
def validate_required_fields(data, fields):
    """Check if all required fields exist in data dict."""
    for field in fields:
        if field not in data:
            return field
    return None

def get_paginated_queryset(queryset, page, page_size):
    """Return paginated queryset and indices info."""
    total_count = queryset.count()
    start = (page - 1) * page_size
    end = start + page_size
    return queryset[start:end], total_count, start, end

# ====== Views ======

class MarhalaWithCountsView(APIView):
    """মারহালা উইথ কাউন্টস ভিউ - ফ্রন্টএন্ডের জন্য ডেটা প্রদান"""
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            cache_key = SubjectCache.MARHALA_WITH_COUNTS_KEY
            cached_data = SubjectCache.get_cache(cache_key)
            if cached_data:
                return Response({
                    'success': True,
                    'data': cached_data,
                    'message': 'মারহালা তালিকা সফলভাবে প্রাপ্ত হয়েছে (ক্যাশ থেকে)',
                    'cached': True
                }, status=status.HTTP_200_OK)
            marhalas = Marhala.objects.annotate(
                total_subjects=Count('subjects'),
                male_subjects=Count('subjects', filter=Q(subjects__status='SRtype_1')),
                female_subjects=Count('subjects', filter=Q(subjects__status='SRtype_0')),
                both_subjects=Count('subjects', filter=Q(subjects__status='both'))
            ).order_by('id')
            serializer = MarhalaWithCountsSerializer(marhalas, many=True)
            SubjectCache.set_cache(cache_key, serializer.data, settings.CACHE_TIMEOUT_MEDIUM)
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'মারহালা তালিকা সফলভাবে প্রাপ্ত হয়েছে',
                'cached': False
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False, 'data': [],
                'message': f'ডেটা প্রাপ্তিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarhalaListView(APIView):
    """মারহালা তালিকা ভিউ"""
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            cache_key = SubjectCache.MARHALA_LIST_KEY
            cached_data = SubjectCache.get_cache(cache_key)
            if cached_data:
                return Response({
                    'success': True, 'data': cached_data,
                    'message': 'মারহালা তালিকা সফলভাবে প্রাপ্ত হয়েছে (ক্যাশ থেকে)', 'cached': True
                }, status=status.HTTP_200_OK)
            marhalas = Marhala.objects.all().order_by('id')
            serializer = MarhalaSerializer(marhalas, many=True)
            SubjectCache.set_cache(cache_key, serializer.data, settings.CACHE_TIMEOUT_LONG)
            return Response({
                'success': True, 'data': serializer.data,
                'message': 'মারহালা তালিকা সফলভাবে প্রাপ্ত হয়েছে', 'cached': False
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False, 'data': [],
                'message': f'ডেটা প্রাপ্তিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarhalaSubjectListView(APIView):
    """মারহালা সাবজেক্ট তালিকা ভিউ"""
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            marhala_id = request.query_params.get('marhala_id')
            if marhala_id:
                subjects = MarhalaSubject.objects.filter(marhala_id=marhala_id).order_by('name_bangla')
            else:
                subjects = MarhalaSubject.objects.all().order_by('marhala_id', 'name_bangla')
            serializer = MarhalaSubjectSerializer(subjects, many=True)
            return Response({
                'success': True, 'data': serializer.data,
                'message': 'সাবজেক্ট তালিকা সফলভাবে প্রাপ্ত হয়েছে'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False, 'data': [],
                'message': f'ডেটা প্রাপ্তিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarhalaSubjectCreateView(APIView):
    """মারহালা সাবজেক্ট তৈরি ভিউ"""
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            serializer = MarhalaSubjectSerializer(data=request.data)
            if serializer.is_valid():
                subject = serializer.save()
                SubjectCache.invalidate_pattern_cache('marhala:*')
                return Response({
                    'success': True, 'data': MarhalaSubjectSerializer(subject).data,
                    'message': 'সাবজেক্ট সফলভাবে তৈরি হয়েছে'
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'success': False, 'data': serializer.errors,
                    'message': 'ডেটা ভ্যালিডেশন ত্রুটি'
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False, 'data': {},
                'message': f'সাবজেক্ট তৈরিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarhalaWithSubjectsCreateView(APIView):
    """মারহালা এবং সাবজেক্ট একসাথে তৈরি করার ভিউ"""
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data = request.data
            required_fields = ['marhala_name_bn', 'marhala_name_en', 'marhala_name_ar', 'subjects']
            missing = validate_required_fields(data, required_fields)
            if missing:
                return Response({
                    'success': False, 'message': f'প্রয়োজনীয় ফিল্ড অনুপস্থিত: {missing}'
                }, status=status.HTTP_400_BAD_REQUEST)
            with transaction.atomic():
                marhala = Marhala.objects.create(
                    marhala_name_bn=data['marhala_name_bn'],
                    marhala_name_en=data['marhala_name_en'],
                    marhala_name_ar=data['marhala_name_ar']
                )
                subjects_data = [
                    MarhalaSubject(
                        marhala=marhala,
                        subject_code=s.get('subject_code', ''),
                        name_bangla=s.get('name_bangla', ''),
                        name_english=s.get('name_english', ''),
                        name_arabic=s.get('name_arabic', ''),
                        status=s.get('status', 'both')
                    )
                    for s in data['subjects'] if s.get('subject_code') and s.get('name_bangla')
                ]
                subjects_created = MarhalaSubject.objects.bulk_create(subjects_data)
                SubjectCache.invalidate_pattern_cache('marhala:*')
                return Response({
                    'success': True,
                    'data': {
                        'marhala': MarhalaSerializer(marhala).data,
                        'subjects': MarhalaSubjectSerializer(subjects_created, many=True).data
                    },
                    'message': f'মারহালা "{marhala.marhala_name_bn}" এবং {len(subjects_created)}টি সাবজেক্ট সফলভাবে তৈরি হয়েছে'
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'success': False, 'data': {},
                'message': f'ডেটা তৈরিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarhalaDetailView(APIView):
    """মারহালা বিস্তারিত ভিউ - একটি নির্দিষ্ট মারহালা ও তার সাবজেক্ট"""
    permission_classes = [AllowAny]
    def get(self, request, marhala_id):
        try:
            marhala = Marhala.objects.get(id=marhala_id)
            subjects = MarhalaSubject.objects.filter(marhala=marhala)
            return Response({
                'success': True,
                'data': {
                    'marhala': MarhalaSerializer(marhala).data,
                    'subjects': MarhalaSubjectSerializer(subjects, many=True).data
                },
                'message': 'মারহালা তথ্য সফলভাবে প্রাপ্ত হয়েছে'
            }, status=status.HTTP_200_OK)
        except Marhala.DoesNotExist:
            return Response({
                'success': False, 'data': {},
                'message': 'মারহালা পাওয়া যায়নি'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False, 'data': {},
                'message': f'ডেটা প্রাপ্তিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarhalaUpdateView(APIView):
    """মারহালা আপডেট ভিউ"""
    permission_classes = [IsAuthenticated]
    def put(self, request, marhala_id):
        try:
            data = request.data
            required_fields = ['marhala_name_bn', 'marhala_name_en', 'marhala_name_ar', 'subjects']
            missing = validate_required_fields(data, required_fields)
            if missing:
                return Response({
                    'success': False, 'message': f'প্রয়োজনীয় ফিল্ড অনুপস্থিত: {missing}'
                }, status=status.HTTP_400_BAD_REQUEST)
            with transaction.atomic():
                marhala = Marhala.objects.get(id=marhala_id)
                marhala.marhala_name_bn = data['marhala_name_bn']
                marhala.marhala_name_en = data['marhala_name_en']
                marhala.marhala_name_ar = data['marhala_name_ar']
                marhala.save()
                existing_subjects = {sub.id: sub for sub in MarhalaSubject.objects.filter(marhala=marhala)}
                processed_subject_ids = set()
                subjects_created = []
                for subject_data in data['subjects']:
                    if not subject_data.get('subject_code') or not subject_data.get('name_bangla'):
                        continue
                    subject_id = subject_data.get('id')
                    if subject_id and subject_id in existing_subjects:
                        subject = existing_subjects[subject_id]
                        subject.subject_code = subject_data.get('subject_code', '')
                        subject.name_bangla = subject_data.get('name_bangla', '')
                        subject.name_english = subject_data.get('name_english', '')
                        subject.name_arabic = subject_data.get('name_arabic', '')
                        subject.status = subject_data.get('status', 'both')
                        subject.save()
                        processed_subject_ids.add(subject_id)
                        subjects_created.append(subject)
                    else:
                        subject = MarhalaSubject.objects.create(
                            marhala=marhala,
                            subject_code=subject_data.get('subject_code', ''),
                            name_bangla=subject_data.get('name_bangla', ''),
                            name_english=subject_data.get('name_english', ''),
                            name_arabic=subject_data.get('name_arabic', ''),
                            status=subject_data.get('status', 'both')
                        )
                        subjects_created.append(subject)
                subjects_to_delete = [sid for sid in existing_subjects.keys() if sid not in processed_subject_ids]
                if subjects_to_delete:
                    MarhalaSubject.objects.filter(id__in=subjects_to_delete).delete()
                SubjectCache.invalidate_pattern_cache('marhala:*')
                SubjectCache.invalidate_pattern_cache('subject_settings:*')
                return Response({
                    'success': True,
                    'data': {
                        'marhala': MarhalaSerializer(marhala).data,
                        'subjects': MarhalaSubjectSerializer(subjects_created, many=True).data
                    },
                    'message': f'মারহালা "{marhala.marhala_name_bn}" সফলভাবে আপডেট হয়েছে'
                }, status=status.HTTP_200_OK)
        except Marhala.DoesNotExist:
            return Response({
                'success': False, 'data': {},
                'message': 'মারহালা পাওয়া যায়নি'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False, 'data': {},
                'message': f'ডেটা আপডেটে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarhalaDeleteView(APIView):
    """মারহালা ডিলিট ভিউ"""
    permission_classes = [IsAuthenticated]
    def delete(self, request, marhala_id):
        try:
            with transaction.atomic():
                marhala = Marhala.objects.get(id=marhala_id)
                marhala_name = marhala.marhala_name_bn
                MarhalaSubject.objects.filter(marhala=marhala).delete()
                marhala.delete()
                SubjectCache.invalidate_pattern_cache('marhala:*')
                SubjectCache.invalidate_pattern_cache('subject_settings:*')
                return Response({
                    'success': True, 'data': {},
                    'message': f'মারহালা "{marhala_name}" সফলভাবে ডিলিট হয়েছে'
                }, status=status.HTTP_200_OK)
        except Marhala.DoesNotExist:
            return Response({
                'success': False, 'data': {},
                'message': 'মারহালা পাওয়া যায়নি'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False, 'data': {},
                'message': f'ডেটা ডিলিটে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubjectSettingsListView(APIView):
    """সাবজেক্ট সেটিংস তালিকা ভিউ"""
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            marhala_id = request.query_params.get('marhala_id')
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 100))
            cache_params = {'marhala_id': marhala_id or 'all', 'page': page, 'page_size': page_size}
            cache_key = SubjectCache.generate_query_key(SubjectCache.SUBJECT_SETTINGS_LIST_KEY, cache_params)
            cached_data = SubjectCache.get_cache(cache_key)
            if cached_data:
                return Response({
                    'success': True, 'data': cached_data['data'], 'pagination': cached_data['pagination'],
                    'message': 'সাবজেক্ট সেটিংস তালিকা সফলভাবে প্রাপ্ত হয়েছে (ক্যাশ থেকে)', 'cached': True
                }, status=status.HTTP_200_OK)
            settings = SubjectSettings.objects.select_related('marhala', 'subject').only(
                'id', 'marhala_id', 'subject_id', 'marhala_type', 'subject_names',
                'student_type', 'syllabus_type', 'markaz_type', 'subject_type',
                'total_marks', 'pass_marks', 'status', 'subject_code',
                'marhala__id', 'marhala__marhala_name_bn',
                'subject__id', 'subject__subject_code'
            ).order_by('marhala_id', 'subject_code')
            if marhala_id:
                settings = settings.filter(marhala_id=marhala_id)
            paginated, total_count, start, end = get_paginated_queryset(settings, page, page_size)
            serializer_data = list(paginated.values(
                'id', 'marhala_id', 'subject_id', 'marhala_type', 'subject_names',
                'student_type', 'syllabus_type', 'markaz_type', 'subject_type',
                'total_marks', 'pass_marks', 'status', 'subject_code',
                'marhala__marhala_name_bn', 'subject__subject_code'
            ))
            formatted_data = [{
                'id': item['id'],
                'marhala': item['marhala_id'],
                'subject': item['subject_id'],
                'marhala_id': item['marhala_id'],
                'subject_id': item['subject_id'],
                'marhala_name': item['marhala__marhala_name_bn'],
                'related_subject_code': item['subject__subject_code'],
                'marhala_type': item['marhala_type'],
                'subject_names': item['subject_names'],
                'student_type': item['student_type'],
                'syllabus_type': item['syllabus_type'],
                'markaz_type': item['markaz_type'],
                'subject_type': item['subject_type'],
                'total_marks': item['total_marks'],
                'pass_marks': item['pass_marks'],
                'status': item['status'],
                'subject_code': item['subject_code']
            } for item in serializer_data]
            pagination_info = {
                'current_page': page,
                'page_size': page_size,
                'total_count': total_count,
                'total_pages': (total_count + page_size - 1) // page_size,
                'has_next': end < total_count,
                'has_previous': page > 1
            }
            response_data = {'data': formatted_data, 'pagination': pagination_info}
            timeout = SubjectCache.CACHE_TIMEOUT_SHORT if marhala_id else SubjectCache.CACHE_TIMEOUT_MEDIUM
            SubjectCache.set_cache(cache_key, response_data, timeout)
            return Response({
                'success': True, 'data': formatted_data, 'pagination': pagination_info,
                'message': 'সাবজেক্ট সেটিংস তালিকা সফলভাবে প্রাপ্ত হয়েছে', 'cached': False
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False, 'data': [],
                'message': f'ডেটা প্রাপ্তিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubjectSettingsCreateView(APIView):
    """সাবজেক্ট সেটিংস তৈরি ভিউ"""
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            serializer = SubjectSettingsSerializer(data=request.data)
            if serializer.is_valid():
                settings = serializer.save()
                SubjectCache.invalidate_pattern_cache('subject_settings:*')
                SubjectCache.invalidate_pattern_cache('marhala:*')
                return Response({
                    'success': True,
                    'data': SubjectSettingsSerializer(settings).data,
                    'message': 'সাবজেক্ট সেটিংস সফলভাবে তৈরি হয়েছে'
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'success': False, 'data': serializer.errors,
                    'message': 'ডেটা ভ্যালিডেশন ত্রুটি'
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False, 'data': {},
                'message': f'সাবজেক্ট সেটিংস তৈরিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubjectSettingsDetailView(APIView):
    """সাবজেক্ট সেটিংস বিস্তারিত ভিউ"""
    permission_classes = [AllowAny]
    def get(self, request, settings_id):
        try:
            cache_key = SubjectCache.generate_key_with_params(
                SubjectCache.SUBJECT_SETTING_DETAIL_KEY, id=settings_id
            )
            cached_data = SubjectCache.get_cache(cache_key)
            if cached_data:
                return Response({
                    'success': True, 'data': cached_data,
                    'message': 'সাবজেক্ট সেটিংস তথ্য সফলভাবে প্রাপ্ত হয়েছে (ক্যাশ থেকে)', 'cached': True
                }, status=status.HTTP_200_OK)
            settings = SubjectSettings.objects.select_related('marhala', 'subject').get(id=settings_id)
            serializer = SubjectSettingsSerializer(settings)
            response_data = {'subject_setting': serializer.data}
            SubjectCache.set_cache(cache_key, response_data, SubjectCache.CACHE_TIMEOUT_MEDIUM)
            return Response({
                'success': True, 'data': response_data,
                'message': 'সাবজেক্ট সেটিংস তথ্য সফলভাবে প্রাপ্ত হয়েছে', 'cached': False
            }, status=status.HTTP_200_OK)
        except SubjectSettings.DoesNotExist:
            return Response({
                'success': False, 'data': {},
                'message': 'সাবজেক্ট সেটিংস পাওয়া যায়নি'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False, 'data': {},
                'message': f'ডেটা প্রাপ্তিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubjectSettingsUpdateView(APIView):
    """সাবজেক্ট সেটিংস আপডেট ভিউ"""
    permission_classes = [IsAuthenticated]
    def put(self, request, settings_id):
        try:
            settings = SubjectSettings.objects.get(id=settings_id)
            serializer = SubjectSettingsSerializer(settings, data=request.data)
            if serializer.is_valid():
                settings = serializer.save()
                SubjectCache.invalidate_pattern_cache('subject_settings:*')
                SubjectCache.invalidate_pattern_cache('marhala:*')
                detail_cache_key = SubjectCache.generate_key_with_params(
                    SubjectCache.SUBJECT_SETTING_DETAIL_KEY, id=settings_id
                )
                SubjectCache.delete_cache(detail_cache_key)
                return Response({
                    'success': True,
                    'data': SubjectSettingsSerializer(settings).data,
                    'message': 'সাবজেক্ট সেটিংস সফলভাবে আপডেট হয়েছে'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False, 'data': serializer.errors,
                    'message': 'ডেটা ভ্যালিডেশন ত্রুটি'
                }, status=status.HTTP_400_BAD_REQUEST)
        except SubjectSettings.DoesNotExist:
            return Response({
                'success': False, 'data': {},
                'message': 'সাবজেক্ট সেটিংস পাওয়া যায়নি'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False, 'data': {},
                'message': f'সাবজেক্ট সেটিংস আপডেটে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubjectSettingsDeleteView(APIView):
    """সাবজেক্ট সেটিংস ডিলিট ভিউ"""
    permission_classes = [IsAuthenticated]
    def delete(self, request, settings_id):
        try:
            settings = SubjectSettings.objects.get(id=settings_id)
            settings.delete()
            SubjectCache.invalidate_pattern_cache('subject_settings:*')
            SubjectCache.invalidate_pattern_cache('marhala:*')
            detail_cache_key = SubjectCache.generate_key_with_params(
                SubjectCache.SUBJECT_SETTING_DETAIL_KEY, id=settings_id
            )
            SubjectCache.delete_cache(detail_cache_key)
            return Response({
                'success': True, 'data': {},
                'message': 'সাবজেক্ট সেটিংস সফলভাবে ডিলিট হয়েছে'
            }, status=status.HTTP_200_OK)
        except SubjectSettings.DoesNotExist:
            return Response({
                'success': False, 'data': {},
                'message': 'সাবজেক্ট সেটিংস পাওয়া যায়নি'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False, 'data': {},
                'message': f'সাবজেক্ট সেটিংস ডিলিটে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetSubjectDataView(APIView):
    """মারহালা অনুযায়ী সাবজেক্ট তথ্য প্রদান - Laravel getsubjecData এর মতো"""
    permission_classes = [AllowAny]
    def get(self, request, marhala_id):
        try:
            cache_key = SubjectCache.generate_key_with_params(
                SubjectCache.MARHALA_SUBJECTS_KEY, id=marhala_id
            )
            cached_data = SubjectCache.get_cache(cache_key)
            if cached_data:
                return Response({
                    'success': True, 'data': cached_data,
                    'message': 'মারহালা ও সাবজেক্ট তথ্য সফলভাবে প্রাপ্ত হয়েছে (ক্যাশ থেকে)', 'cached': True
                }, status=status.HTTP_200_OK)
            marhala = Marhala.objects.values('id', 'marhala_name_bn').get(id=marhala_id)
            subjects = MarhalaSubject.objects.filter(marhala_id=marhala_id).values(
                'id', 'name_bangla', 'subject_code'
            )
            response_data = {'marhala': marhala, 'subjects': list(subjects)}
            SubjectCache.set_cache(cache_key, response_data, settings.CACHE_TIMEOUT_MEDIUM)
            return Response({
                'success': True, 'data': response_data,
                'message': 'মারহালা ও সাবজেক্ট তথ্য সফলভাবে প্রাপ্ত হয়েছে', 'cached': False
            }, status=status.HTTP_200_OK)
        except Marhala.DoesNotExist:
            return Response({
                'success': False, 'data': {},
                'message': 'মারহালা পাওয়া যায়নি'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False, 'data': {},
                'message': f'ডেটা প্রাপ্তিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateSubjectSettingView(APIView):
    """সাবজেক্ট সেটিংস আপডেট - POST & PUT"""
    permission_classes = [IsAuthenticated]
    def post(self, request, settings_id):
        try:
            required_fields = [
                'marhala_id', 'subject_id', 'marhala_type', 'subject_names',
                'student_type', 'syllabus_type', 'markaz_type', 'subject_type',
                'total_marks', 'pass_marks', 'status'
            ]
            missing = validate_required_fields(request.data, required_fields)
            if missing:
                return Response({
                    'success': False, 'data': {},
                    'message': f'{missing} ফিল্ড আবশ্যক'
                }, status=status.HTTP_400_BAD_REQUEST)
            if request.data['status'] not in ['active', 'inactive']:
                return Response({
                    'success': False, 'data': {},
                    'message': 'স্ট্যাটাস active অথবা inactive হতে হবে'
                }, status=status.HTTP_400_BAD_REQUEST)
            subject_setting = SubjectSettings.objects.get(id=settings_id)
            for field in required_fields + ['subject_code']:
                if field in request.data:
                    setattr(subject_setting, field, request.data[field])
            subject_setting.save()
            SubjectCache.invalidate_pattern_cache('subject_settings:*')
            SubjectCache.invalidate_pattern_cache('marhala:*')
            detail_cache_key = SubjectCache.generate_key_with_params(
                SubjectCache.SUBJECT_SETTING_DETAIL_KEY, id=settings_id
            )
            SubjectCache.delete_cache(detail_cache_key)
            return Response({
                'success': True, 'data': {},
                'message': 'বিষয় সেটাপ সঠিকভাবে আপডেট করা হয়েছে'
            }, status=status.HTTP_200_OK)
        except SubjectSettings.DoesNotExist:
            return Response({
                'success': False, 'data': {},
                'message': 'সাবজেক্ট সেটিংস পাওয়া যায়নি'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False, 'data': {},
                'message': f'সাবজেক্ট সেটিংস আপডেটে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self, request, settings_id):
        return self.post(request, settings_id)


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