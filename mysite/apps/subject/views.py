from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db.models import Count, Q
from django.db import transaction
from django.conf import settings
from .models import Marhala, MarhalaSubject, SubjectSettings
from .serializers import MarhalaWithCountsSerializer, MarhalaSerializer, MarhalaSubjectSerializer, SubjectSettingsSerializer
from .cache import SubjectCache


class MarhalaWithCountsView(APIView):
    """মারহালা উইথ কাউন্টস ভিউ - ফ্রন্টএন্ডের জন্য ডেটা প্রদান"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """মারহালা তালিকা কাউন্টস সহ ফেরত দেয়"""
        try:
            # Try to get from cache first
            cache_key = SubjectCache.MARHALA_WITH_COUNTS_KEY
            cached_data = SubjectCache.get_cache(cache_key)
            
            if cached_data:
                return Response({
                    'success': True,
                    'data': cached_data,
                    'message': 'মারহালা তালিকা সফলভাবে প্রাপ্ত হয়েছে (ক্যাশ থেকে)',
                    'cached': True
                }, status=status.HTTP_200_OK)
            
            # Django ORM দিয়ে counts সহ data fetch
            marhalas = Marhala.objects.annotate(
                total_subjects=Count('subjects'),
                male_subjects=Count('subjects', filter=Q(subjects__status='SRtype_1')),
                female_subjects=Count('subjects', filter=Q(subjects__status='SRtype_0')),
                both_subjects=Count('subjects', filter=Q(subjects__status='both'))
            ).order_by('id')
            
            serializer = MarhalaWithCountsSerializer(marhalas, many=True)
            
            # Cache the result
            SubjectCache.set_cache(cache_key, serializer.data, settings.CACHE_TIMEOUT_MEDIUM)
            
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'মারহালা তালিকা সফলভাবে প্রাপ্ত হয়েছে',
                'cached': False
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'data': [],
                'message': f'ডেটা প্রাপ্তিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarhalaListView(APIView):
    """মারহালা তালিকা ভিউ"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """সব মারহালার তালিকা ফেরত দেয়"""
        try:
            # Try to get from cache first
            cache_key = SubjectCache.MARHALA_LIST_KEY
            cached_data = SubjectCache.get_cache(cache_key)
            
            if cached_data:
                return Response({
                    'success': True,
                    'data': cached_data,
                    'message': 'মারহালা তালিকা সফলভাবে প্রাপ্ত হয়েছে (ক্যাশ থেকে)',
                    'cached': True
                }, status=status.HTTP_200_OK)
            
            marhalas = Marhala.objects.all().order_by('id')
            serializer = MarhalaSerializer(marhalas, many=True)
            
            # Cache the result
            SubjectCache.set_cache(cache_key, serializer.data, settings.CACHE_TIMEOUT_LONG)
            
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'মারহালা তালিকা সফলভাবে প্রাপ্ত হয়েছে',
                'cached': False
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'data': [],
                'message': f'ডেটা প্রাপ্তিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarhalaSubjectListView(APIView):
    """মারহালা সাবজেক্ট তালিকা ভিউ"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """নির্দিষ্ট মারহালার সাবজেক্ট তালিকা ফেরত দেয়"""
        try:
            marhala_id = request.query_params.get('marhala_id')
            
            if marhala_id:
                subjects = MarhalaSubject.objects.filter(
                    marhala_id=marhala_id
                ).order_by('name_bangla')
            else:
                subjects = MarhalaSubject.objects.all().order_by('marhala_id', 'name_bangla')
            
            serializer = MarhalaSubjectSerializer(subjects, many=True)
            
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'সাবজেক্ট তালিকা সফলভাবে প্রাপ্ত হয়েছে'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'data': [],
                'message': f'ডেটা প্রাপ্তিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarhalaSubjectCreateView(APIView):
    """মারহালা সাবজেক্ট তৈরি ভিউ"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """নতুন সাবজেক্ট তৈরি করে"""
        try:
            serializer = MarhalaSubjectSerializer(data=request.data)
            
            if serializer.is_valid():
                subject = serializer.save()
                return Response({
                    'success': True,
                    'data': MarhalaSubjectSerializer(subject).data,
                    'message': 'সাবজেক্ট সফলভাবে তৈরি হয়েছে'
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'success': False,
                    'data': serializer.errors,
                    'message': 'ডেটা ভ্যালিডেশন ত্রুটি'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                'success': False,
                'data': {},
                'message': f'সাবজেক্ট তৈরিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarhalaWithSubjectsCreateView(APIView):
    """মারহালা এবং সাবজেক্ট একসাথে তৈরি করার ভিউ"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """নতুন মারহালা এবং তার সাবজেক্টগুলো একসাথে তৈরি করে"""
        try:
            data = request.data
            
            # Validate required fields
            required_fields = ['marhala_name_bn', 'marhala_name_en', 'marhala_name_ar', 'subjects']
            for field in required_fields:
                if field not in data:
                    return Response({
                        'success': False,
                        'message': f'প্রয়োজনীয় ফিল্ড অনুপস্থিত: {field}'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            with transaction.atomic():
                # Create Marhala using Django ORM
                marhala = Marhala.objects.create(
                    marhala_name_bn=data['marhala_name_bn'],
                    marhala_name_en=data['marhala_name_en'],
                    marhala_name_ar=data['marhala_name_ar']
                )
                
                # Create Subjects using Django ORM
                subjects_created = []
                for subject_data in data['subjects']:
                    # Skip empty subjects
                    if not subject_data.get('subject_code') or not subject_data.get('name_bangla'):
                        continue
                    
                    subject = MarhalaSubject.objects.create(
                        marhala=marhala,
                        subject_code=subject_data.get('subject_code', ''),
                        name_bangla=subject_data.get('name_bangla', ''),
                        name_english=subject_data.get('name_english', ''),
                        name_arabic=subject_data.get('name_arabic', ''),
                        status=subject_data.get('status', 'both')
                    )
                    subjects_created.append(subject)
                
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
                'success': False,
                'data': {},
                'message': f'ডেটা তৈরিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarhalaDetailView(APIView):
    """মারহালা বিস্তারিত ভিউ - একটি নির্দিষ্ট মারহালা ও তার সাবজেক্ট"""
    permission_classes = [AllowAny]
    
    def get(self, request, marhala_id):
        """নির্দিষ্ট মারহালার তথ্য ও সাবজেক্ট ফেরত দেয়"""
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
                'success': False,
                'data': {},
                'message': 'মারহালা পাওয়া যায়নি'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'data': {},
                'message': f'ডেটা প্রাপ্তিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarhalaUpdateView(APIView):
    """মারহালা আপডেট ভিউ"""
    permission_classes = [AllowAny]
    
    def put(self, request, marhala_id):
        """মারহালা ও তার সাবজেক্ট আপডেট করে"""
        try:
            data = request.data
            
            # Validate required fields
            required_fields = ['marhala_name_bn', 'marhala_name_en', 'marhala_name_ar', 'subjects']
            for field in required_fields:
                if field not in data:
                    return Response({
                        'success': False,
                        'message': f'প্রয়োজনীয় ফিল্ড অনুপস্থিত: {field}'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            with transaction.atomic():
                # Update Marhala
                marhala = Marhala.objects.get(id=marhala_id)
                marhala.marhala_name_bn = data['marhala_name_bn']
                marhala.marhala_name_en = data['marhala_name_en']
                marhala.marhala_name_ar = data['marhala_name_ar']
                marhala.save()
                
                # Get existing subjects
                existing_subjects = MarhalaSubject.objects.filter(marhala=marhala)
                existing_subjects_dict = {sub.id: sub for sub in existing_subjects}
                
                # Process new subjects data
                processed_subject_ids = set()
                subjects_created = []
                
                for subject_data in data['subjects']:
                    # Skip empty subjects
                    if not subject_data.get('subject_code') or not subject_data.get('name_bangla'):
                        continue
                    
                    subject_id = subject_data.get('id')
                    
                    if subject_id and subject_id in existing_subjects_dict:
                        # Update existing subject
                        subject = existing_subjects_dict[subject_id]
                        subject.subject_code = subject_data.get('subject_code', '')
                        subject.name_bangla = subject_data.get('name_bangla', '')
                        subject.name_english = subject_data.get('name_english', '')
                        subject.name_arabic = subject_data.get('name_arabic', '')
                        subject.status = subject_data.get('status', 'both')
                        subject.save()
                        processed_subject_ids.add(subject_id)
                    else:
                        # Create new subject
                        subject = MarhalaSubject.objects.create(
                            marhala=marhala,
                            subject_code=subject_data.get('subject_code', ''),
                            name_bangla=subject_data.get('name_bangla', ''),
                            name_english=subject_data.get('name_english', ''),
                            name_arabic=subject_data.get('name_arabic', ''),
                            status=subject_data.get('status', 'both')
                        )
                    
                    subjects_created.append(subject)
                
                # Delete subjects that are no longer needed
                subjects_to_delete = [sid for sid in existing_subjects_dict.keys() if sid not in processed_subject_ids]
                if subjects_to_delete:
                    MarhalaSubject.objects.filter(id__in=subjects_to_delete).delete()
                
                # Invalidate relevant caches after updating marhala and subjects
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
                'success': False,
                'data': {},
                'message': 'মারহালা পাওয়া যায়নি'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'data': {},
                'message': f'ডেটা আপডেটে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarhalaDeleteView(APIView):
    """মারহালা ডিলিট ভিউ"""
    permission_classes = [AllowAny]
    
    def delete(self, request, marhala_id):
        """মারহালা ও তার সাবজেক্ট ডিলিট করে"""
        try:
            with transaction.atomic():
                marhala = Marhala.objects.get(id=marhala_id)
                marhala_name = marhala.marhala_name_bn
                
                # Delete subjects first (cascade will handle this, but explicit is better)
                MarhalaSubject.objects.filter(marhala=marhala).delete()
                
                # Delete marhala
                marhala.delete()
                
                # Invalidate relevant caches after deleting marhala
                SubjectCache.invalidate_pattern_cache('marhala:*')
                SubjectCache.invalidate_pattern_cache('subject_settings:*')
                
                return Response({
                    'success': True,
                    'data': {},
                    'message': f'মারহালা "{marhala_name}" সফলভাবে ডিলিট হয়েছে'
                }, status=status.HTTP_200_OK)
                
        except Marhala.DoesNotExist:
            return Response({
                'success': False,
                'data': {},
                'message': 'মারহালা পাওয়া যায়নি'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'data': {},
                'message': f'ডেটা ডিলিটে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubjectSettingsListView(APIView):
    """সাবজেক্ট সেটিংস তালিকা ভিউ"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """সব সাবজেক্ট সেটিংসের তালিকা ফেরত দেয়"""
        try:
            marhala_id = request.query_params.get('marhala_id')
            
            # Generate cache key based on query parameters
            if marhala_id:
                cache_key = SubjectCache.generate_key_with_params(
                    SubjectCache.SUBJECT_SETTINGS_BY_MARHALA_KEY, 
                    marhala_id=marhala_id
                )
            else:
                cache_key = SubjectCache.SUBJECT_SETTINGS_LIST_KEY
            
            # Try to get from cache first
            cached_data = SubjectCache.get_cache(cache_key)
            
            if cached_data:
                return Response({
                    'success': True,
                    'data': cached_data,
                    'message': 'সাবজেক্ট সেটিংস তালিকা সফলভাবে প্রাপ্ত হয়েছে (ক্যাশ থেকে)',
                    'cached': True
                }, status=status.HTTP_200_OK)
            
            settings = SubjectSettings.objects.select_related(
                'marhala', 'subject'
            ).order_by('marhala_id', 'subject_code')
            
            if marhala_id:
                settings = settings.filter(marhala_id=marhala_id)
            
            serializer = SubjectSettingsSerializer(settings, many=True)
            
            # Cache the result
            timeout = SubjectCache.CACHE_TIMEOUT_SHORT if marhala_id else SubjectCache.CACHE_TIMEOUT_MEDIUM
            SubjectCache.set_cache(cache_key, serializer.data, timeout)
            
            return Response({
                'success': True,
                'data': serializer.data,
                'message': 'সাবজেক্ট সেটিংস তালিকা সফলভাবে প্রাপ্ত হয়েছে',
                'cached': False
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'data': [],
                'message': f'ডেটা প্রাপ্তিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubjectSettingsCreateView(APIView):
    """সাবজেক্ট সেটিংস তৈরি ভিউ"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """নতুন সাবজেক্ট সেটিংস তৈরি করে"""
        try:
            serializer = SubjectSettingsSerializer(data=request.data)
            
            if serializer.is_valid():
                settings = serializer.save()
                
                # Invalidate relevant caches after creating new subject settings
                SubjectCache.invalidate_pattern_cache('subject_settings:*')
                SubjectCache.invalidate_pattern_cache('marhala:*')
                
                return Response({
                    'success': True,
                    'data': SubjectSettingsSerializer(settings).data,
                    'message': 'সাবজেক্ট সেটিংস সফলভাবে তৈরি হয়েছে'
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'success': False,
                    'data': serializer.errors,
                    'message': 'ডেটা ভ্যালিডেশন ত্রুটি'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                'success': False,
                'data': {},
                'message': f'সাবজেক্ট সেটিংস তৈরিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubjectSettingsDetailView(APIView):
    """সাবজেক্ট সেটিংস বিস্তারিত ভিউ"""
    permission_classes = [AllowAny]
    
    def get(self, request, settings_id):
        """নির্দিষ্ট সাবজেক্ট সেটিংসের তথ্য ফেরত দেয়"""
        try:
            # Generate cache key for specific subject setting
            cache_key = SubjectCache.generate_key_with_params(
                SubjectCache.SUBJECT_SETTING_DETAIL_KEY, 
                id=settings_id
            )
            
            # Try to get from cache first
            cached_data = SubjectCache.get_cache(cache_key)
            
            if cached_data:
                return Response({
                    'success': True,
                    'data': cached_data,
                    'message': 'সাবজেক্ট সেটিংস তথ্য সফলভাবে প্রাপ্ত হয়েছে (ক্যাশ থেকে)',
                    'cached': True
                }, status=status.HTTP_200_OK)
            
            settings = SubjectSettings.objects.select_related(
                'marhala', 'subject'
            ).get(id=settings_id)
            
            serializer = SubjectSettingsSerializer(settings)
            response_data = {
                'subject_setting': serializer.data
            }
            
            # Cache the result
            SubjectCache.set_cache(cache_key, response_data, SubjectCache.CACHE_TIMEOUT_MEDIUM)
            
            return Response({
                'success': True,
                'data': response_data,
                'message': 'সাবজেক্ট সেটিংস তথ্য সফলভাবে প্রাপ্ত হয়েছে',
                'cached': False
            }, status=status.HTTP_200_OK)
            
        except SubjectSettings.DoesNotExist:
            return Response({
                'success': False,
                'data': {},
                'message': 'সাবজেক্ট সেটিংস পাওয়া যায়নি'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'data': {},
                'message': f'ডেটা প্রাপ্তিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubjectSettingsUpdateView(APIView):
    """সাবজেক্ট সেটিংস আপডেট ভিউ"""
    permission_classes = [AllowAny]
    
    def put(self, request, settings_id):
        """সাবজেক্ট সেটিংস আপডেট করে"""
        try:
            settings = SubjectSettings.objects.get(id=settings_id)
            serializer = SubjectSettingsSerializer(settings, data=request.data)
            
            if serializer.is_valid():
                settings = serializer.save()
                
                # Invalidate relevant caches after updating subject settings
                SubjectCache.invalidate_pattern_cache('subject_settings:*')
                SubjectCache.invalidate_pattern_cache('marhala:*')
                
                # Also invalidate the specific setting detail cache
                detail_cache_key = SubjectCache.generate_key_with_params(
                    SubjectCache.SUBJECT_SETTING_DETAIL_KEY, 
                    id=settings_id
                )
                SubjectCache.delete_cache(detail_cache_key)
                
                return Response({
                    'success': True,
                    'data': SubjectSettingsSerializer(settings).data,
                    'message': 'সাবজেক্ট সেটিংস সফলভাবে আপডেট হয়েছে'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'data': serializer.errors,
                    'message': 'ডেটা ভ্যালিডেশন ত্রুটি'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except SubjectSettings.DoesNotExist:
            return Response({
                'success': False,
                'data': {},
                'message': 'সাবজেক্ট সেটিংস পাওয়া যায়নি'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'data': {},
                'message': f'সাবজেক্ট সেটিংস আপডেটে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubjectSettingsDeleteView(APIView):
    """সাবজেক্ট সেটিংস ডিলিট ভিউ"""
    permission_classes = [AllowAny]
    
    def delete(self, request, settings_id):
        """সাবজেক্ট সেটিংস ডিলিট করে"""
        try:
            settings = SubjectSettings.objects.get(id=settings_id)
            settings.delete()
            
            # Invalidate relevant caches after deleting subject settings
            SubjectCache.invalidate_pattern_cache('subject_settings:*')
            SubjectCache.invalidate_pattern_cache('marhala:*')
            
            # Also invalidate the specific setting detail cache
            detail_cache_key = SubjectCache.generate_key_with_params(
                SubjectCache.SUBJECT_SETTING_DETAIL_KEY, 
                id=settings_id
            )
            SubjectCache.delete_cache(detail_cache_key)
            
            return Response({
                'success': True,
                'data': {},
                'message': 'সাবজেক্ট সেটিংস সফলভাবে ডিলিট হয়েছে'
            }, status=status.HTTP_200_OK)
            
        except SubjectSettings.DoesNotExist:
            return Response({
                'success': False,
                'data': {},
                'message': 'সাবজেক্ট সেটিংস পাওয়া যায়নি'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'data': {},
                'message': f'সাবজেক্ট সেটিংস ডিলিটে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetSubjectDataView(APIView):
    """মারহালা অনুযায়ী সাবজেক্ট তথ্য প্রদান - Laravel getsubjecData এর মতো"""
    permission_classes = [AllowAny]
    
    def get(self, request, marhala_id):
        """একটি নির্দিষ্ট মারহালার সব সাবজেক্টের তথ্য ফেরত দেয়"""
        try:
            # Try to get from cache first
            cache_key = SubjectCache.generate_key_with_params(
                SubjectCache.MARHALA_SUBJECTS_KEY, 
                id=marhala_id
            )
            cached_data = SubjectCache.get_cache(cache_key)
            
            if cached_data:
                return Response({
                    'success': True,
                    'data': cached_data,
                    'message': 'মারহালা ও সাবজেক্ট তথ্য সফলভাবে প্রাপ্ত হয়েছে (ক্যাশ থেকে)',
                    'cached': True
                }, status=status.HTTP_200_OK)
            
            # Get marhala details
            marhala = Marhala.objects.values('id', 'marhala_name_bn').get(id=marhala_id)
            
            # Get subjects for this marhala
            subjects = MarhalaSubject.objects.filter(marhala_id=marhala_id).values(
                'id', 'name_bangla', 'subject_code'
            )
            
            response_data = {
                'marhala': marhala,
                'subjects': list(subjects)
            }
            
            # Cache the result
            SubjectCache.set_cache(cache_key, response_data, settings.CACHE_TIMEOUT_MEDIUM)
            
            return Response({
                'success': True,
                'data': response_data,
                'message': 'মারহালা ও সাবজেক্ট তথ্য সফলভাবে প্রাপ্ত হয়েছে',
                'cached': False
            }, status=status.HTTP_200_OK)
            
        except Marhala.DoesNotExist:
            return Response({
                'success': False,
                'data': {},
                'message': 'মারহালা পাওয়া যায়নি'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'data': {},
                'message': f'ডেটা প্রাপ্তিতে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateSubjectSettingView(APIView):
    """সাবজেক্ট সেটিংস আপডেট - Laravel updateSubjectSetting এর মতো"""
    permission_classes = [AllowAny]
    
    def post(self, request, settings_id):
        """সাবজেক্ট সেটিংস আপডেট করে (POST method for frontend compatibility)"""
        try:
            # Validation
            required_fields = [
                'marhala_id', 'subject_id', 'marhala_type', 'subject_names',
                'student_type', 'syllabus_type', 'markaz_type', 'subject_type',
                'total_marks', 'pass_marks', 'status'
            ]
            
            for field in required_fields:
                if field not in request.data:
                    return Response({
                        'success': False,
                        'data': {},
                        'message': f'{field} ফিল্ড আবশ্যক'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if status is valid
            if request.data['status'] not in ['active', 'inactive']:
                return Response({
                    'success': False,
                    'data': {},
                    'message': 'স্ট্যাটাস active অথবা inactive হতে হবে'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Find and update the subject setting
            subject_setting = SubjectSettings.objects.get(id=settings_id)
            
            # Update fields
            subject_setting.marhala_id = request.data['marhala_id']
            subject_setting.subject_id = request.data['subject_id']
            subject_setting.marhala_type = request.data['marhala_type']
            subject_setting.subject_names = request.data['subject_names']
            subject_setting.student_type = request.data['student_type']
            subject_setting.syllabus_type = request.data['syllabus_type']
            subject_setting.markaz_type = request.data['markaz_type']
            subject_setting.subject_type = request.data['subject_type']
            subject_setting.total_marks = request.data['total_marks']
            subject_setting.pass_marks = request.data['pass_marks']
            subject_setting.status = request.data['status']
            
            # Update subject_code if available
            if 'subject_code' in request.data:
                subject_setting.subject_code = request.data['subject_code']
            
            subject_setting.save()
            
            return Response({
                'success': True,
                'data': {},
                'message': 'বিষয় সেটাপ সঠিকভাবে আপডেট করা হয়েছে'
            }, status=status.HTTP_200_OK)
            
        except SubjectSettings.DoesNotExist:
            return Response({
                'success': False,
                'data': {},
                'message': 'সাবজেক্ট সেটিংস পাওয়া যায়নি'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'data': {},
                'message': f'সাবজেক্ট সেটিংস আপডেটে সমস্যা: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, settings_id):
        """সাবজেক্ট সেটিংস আপডেট করে (PUT method)"""
        # Same logic as POST method
        return self.post(request, settings_id)
