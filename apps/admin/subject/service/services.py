import json
from django.db.models import Count, Q
from django.db import transaction
from django.conf import settings
from django.core.cache import cache
from ..models import Marhala, MarhalaSubject, SubjectSettings
from apps.admin.CentralExam.models import ExamFee
from ..serializers import (
    MarhalaWithCountsSerializer, MarhalaSerializer,
    MarhalaSubjectSerializer, SubjectSettingsSerializer
)
from apps.admin.CentralExam.serializers import ExamFeeSerializer
from ..cache import SubjectCache

def validate_required_fields(data, fields):
    for field in fields:
        if field not in data:
            return field
    return None

def get_paginated_queryset(queryset, page, page_size):
    total_count = queryset.count()
    start = (page - 1) * page_size
    end = start + page_size
    return queryset[start:end], total_count, start, end

def get_marhala_with_counts_service():
    cache_key = SubjectCache.MARHALA_WITH_COUNTS_KEY
    cached_data = SubjectCache.get_cache(cache_key)
    if cached_data:
        return cached_data, True
    marhalas = Marhala.objects.annotate(
        total_subjects=Count('subjects'),
        male_subjects=Count('subjects', filter=Q(subjects__status='SRtype_1')),
        female_subjects=Count('subjects', filter=Q(subjects__status='SRtype_0')),
        both_subjects=Count('subjects', filter=Q(subjects__status='both'))
    ).order_by('id')
    serializer = MarhalaWithCountsSerializer(marhalas, many=True)
    SubjectCache.set_cache(cache_key, serializer.data, settings.CACHE_TIMEOUT_MEDIUM)
    return serializer.data, False

def get_marhala_list_service():
    cache_key = SubjectCache.MARHALA_LIST_KEY
    cached_data = SubjectCache.get_cache(cache_key)
    if cached_data:
        return cached_data, True
    marhalas = Marhala.objects.all().order_by('id')
    serializer = MarhalaSerializer(marhalas, many=True)
    SubjectCache.set_cache(cache_key, serializer.data, settings.CACHE_TIMEOUT_LONG)
    return serializer.data, False

def get_marhala_subject_list_service(marhala_id=None):
    if marhala_id:
        subjects = MarhalaSubject.objects.filter(marhala_id=marhala_id).order_by('name_bangla')
    else:
        subjects = MarhalaSubject.objects.all().order_by('marhala_id', 'name_bangla')
    serializer = MarhalaSubjectSerializer(subjects, many=True)
    return serializer.data

def create_marhala_subject_service(data):
    serializer = MarhalaSubjectSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    subject = serializer.save()
    SubjectCache.invalidate_pattern_cache('marhala:*')
    return MarhalaSubjectSerializer(subject).data

def create_marhala_with_subjects_service(data):
    required_fields = ['marhala_name_bn', 'marhala_name_en', 'marhala_name_ar', 'subjects']
    missing = validate_required_fields(data, required_fields)
    if missing:
        return None, None, missing
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
        return MarhalaSerializer(marhala).data, MarhalaSubjectSerializer(subjects_created, many=True).data, None

def get_marhala_detail_service(marhala_id):
    marhala = Marhala.objects.get(id=marhala_id)
    subjects = MarhalaSubject.objects.filter(marhala=marhala)
    return MarhalaSerializer(marhala).data, MarhalaSubjectSerializer(subjects, many=True).data

def update_marhala_service(marhala_id, data):
    required_fields = ['marhala_name_bn', 'marhala_name_en', 'marhala_name_ar', 'subjects']
    missing = validate_required_fields(data, required_fields)
    if missing:
        return None, None, missing
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
        return MarhalaSerializer(marhala).data, MarhalaSubjectSerializer(subjects_created, many=True).data, None

def delete_marhala_service(marhala_id):
    with transaction.atomic():
        marhala = Marhala.objects.get(id=marhala_id)
        marhala_name = marhala.marhala_name_bn
        MarhalaSubject.objects.filter(marhala=marhala).delete()
        marhala.delete()
        SubjectCache.invalidate_pattern_cache('marhala:*')
        SubjectCache.invalidate_pattern_cache('subject_settings:*')
        return marhala_name

def get_subject_settings_list_service(marhala_id=None, page=1, page_size=100):
    cache_params = {'marhala_id': marhala_id or 'all', 'page': page, 'page_size': page_size}
    cache_key = SubjectCache.generate_query_key(SubjectCache.SUBJECT_SETTINGS_LIST_KEY, cache_params)
    cached_data = SubjectCache.get_cache(cache_key)
    if cached_data:
        return cached_data['data'], cached_data['pagination'], True
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
    return formatted_data, pagination_info, False

def create_subject_settings_service(data):
    serializer = SubjectSettingsSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    settings = serializer.save()
    SubjectCache.invalidate_pattern_cache('subject_settings:*')
    SubjectCache.invalidate_pattern_cache('marhala:*')
    return SubjectSettingsSerializer(settings).data

def get_subject_settings_detail_service(settings_id):
    cache_key = SubjectCache.generate_key_with_params(
        SubjectCache.SUBJECT_SETTING_DETAIL_KEY, id=settings_id
    )
    cached_data = SubjectCache.get_cache(cache_key)
    if cached_data:
        return cached_data, True
    settings = SubjectSettings.objects.select_related('marhala', 'subject').get(id=settings_id)
    serializer = SubjectSettingsSerializer(settings)
    response_data = {'subject_setting': serializer.data}
    SubjectCache.set_cache(cache_key, response_data, SubjectCache.CACHE_TIMEOUT_MEDIUM)
    return response_data, False

def update_subject_settings_service(settings_id, data):
    settings = SubjectSettings.objects.get(id=settings_id)
    serializer = SubjectSettingsSerializer(settings, data=data)
    serializer.is_valid(raise_exception=True)
    settings = serializer.save()
    SubjectCache.invalidate_pattern_cache('subject_settings:*')
    SubjectCache.invalidate_pattern_cache('marhala:*')
    detail_cache_key = SubjectCache.generate_key_with_params(
        SubjectCache.SUBJECT_SETTING_DETAIL_KEY, id=settings_id
    )
    SubjectCache.delete_cache(detail_cache_key)
    return SubjectSettingsSerializer(settings).data

def delete_subject_settings_service(settings_id):
    settings = SubjectSettings.objects.get(id=settings_id)
    settings.delete()
    SubjectCache.invalidate_pattern_cache('subject_settings:*')
    SubjectCache.invalidate_pattern_cache('marhala:*')
    detail_cache_key = SubjectCache.generate_key_with_params(
        SubjectCache.SUBJECT_SETTING_DETAIL_KEY, id=settings_id
    )
    SubjectCache.delete_cache(detail_cache_key)
    return True

def get_subject_data_service(marhala_id):
    cache_key = SubjectCache.generate_key_with_params(
        SubjectCache.MARHALA_SUBJECTS_KEY, id=marhala_id
    )
    cached_data = SubjectCache.get_cache(cache_key)
    if cached_data:
        return cached_data, True
    marhala = Marhala.objects.values('id', 'marhala_name_bn').get(id=marhala_id)
    subjects = MarhalaSubject.objects.filter(marhala_id=marhala_id).values(
        'id', 'name_bangla', 'subject_code'
    )
    response_data = {'marhala': marhala, 'subjects': list(subjects)}
    SubjectCache.set_cache(cache_key, response_data, settings.CACHE_TIMEOUT_MEDIUM)
    return response_data, False

def update_subject_setting_service(settings_id, data):
    required_fields = [
        'marhala_id', 'subject_id', 'marhala_type', 'subject_names',
        'student_type', 'syllabus_type', 'markaz_type', 'subject_type',
        'total_marks', 'pass_marks', 'status'
    ]
    missing = validate_required_fields(data, required_fields)
    if missing:
        return False, f'{missing} ফিল্ড আবশ্যক'
    if data['status'] not in ['active', 'inactive']:
        return False, 'স্ট্যাটাস active অথবা inactive হতে হবে'
    subject_setting = SubjectSettings.objects.get(id=settings_id)
    for field in required_fields + ['subject_code']:
        if field in data:
            setattr(subject_setting, field, data[field])
    subject_setting.save()
    SubjectCache.invalidate_pattern_cache('subject_settings:*')
    SubjectCache.invalidate_pattern_cache('marhala:*')
    detail_cache_key = SubjectCache.generate_key_with_params(
        SubjectCache.SUBJECT_SETTING_DETAIL_KEY, id=settings_id
    )
    SubjectCache.delete_cache(detail_cache_key)
    return True, 'বিষয় সেটাপ সঠিকভাবে আপডেট করা হয়েছে'

def get_exam_fee_list_by_setup_service(exam_setup_id):
    cache_key = f"exam_fee_list_{exam_setup_id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return json.loads(cached_data), 'cache'
    fees = ExamFee.objects.filter(exam_setup_id=exam_setup_id).select_related('marhala', 'exam_setup')
    if not fees.exists():
        return [], None
    serializer = ExamFeeSerializer(fees, many=True)
    cache.set(cache_key, json.dumps(serializer.data), timeout=60 * 30)
    return serializer.data, 'database'