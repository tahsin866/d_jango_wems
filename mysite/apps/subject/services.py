from django.db import transaction
from django.conf import settings
from django.core.cache import cache
from django.db.models import Count, Q
import json

from .models import Marhala, MarhalaSubject, SubjectSettings
from mysite.apps.CentralExam.models import ExamFee
from .serializers import (
    MarhalaWithCountsSerializer, MarhalaSerializer,
    MarhalaSubjectSerializer, SubjectSettingsSerializer
)
from mysite.apps.CentralExam.serializers import ExamFeeSerializer
from .cache import SubjectCache


# =========================
# Marhala Services
# =========================

def get_marhala_with_counts():
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


def get_marhala_list():
    cache_key = SubjectCache.MARHALA_LIST_KEY
    cached_data = SubjectCache.get_cache(cache_key)
    if cached_data:
        return cached_data, True

    marhalas = Marhala.objects.all().order_by('id')
    serializer = MarhalaSerializer(marhalas, many=True)
    SubjectCache.set_cache(cache_key, serializer.data, settings.CACHE_TIMEOUT_LONG)
    return serializer.data, False


def get_marhala_subject_list(marhala_id=None):
    """
    মারহালা অনুযায়ী সাবজেক্ট তালিকা রিটার্ন করবে।
    যদি marhala_id দেয়া হয় তাহলে সেই মারহালার সাবজেক্ট রিটার্ন করবে,
    অন্যথায় সব সাবজেক্ট রিটার্ন করবে।
    """
    if marhala_id:
        subjects = MarhalaSubject.objects.filter(marhala_id=marhala_id).order_by('name_bangla')
    else:
        subjects = MarhalaSubject.objects.all().order_by('marhala_id', 'name_bangla')
    serializer = MarhalaSubjectSerializer(subjects, many=True)
    return serializer.data


# =========================
# Exam Fee Services
# =========================

def get_exam_fees_by_setup(exam_setup_id):
    """
    নির্দিষ্ট exam_setup_id এর সব ExamFee রিটার্ন করবে।
    প্রথমে Redis cache চেক করবে, তারপর DB থেকে নেবে।
    """
    cache_key = f"exam_fee_list_{exam_setup_id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return json.loads(cached_data), "cache"

    fees = ExamFee.objects.filter(exam_setup_id=exam_setup_id).select_related('marhala', 'exam_setup')
    if not fees.exists():
        return [], None

    serializer = ExamFeeSerializer(fees, many=True)
    cache.set(cache_key, json.dumps(serializer.data), timeout=60 * 30)
    return serializer.data, "database"


# =========================
# SubjectSettings Services
# =========================

def get_subject_settings_list(marhala_id=None, page=1, page_size=100):
    """
    সাবজেক্ট সেটিংস তালিকা রিটার্ন করবে, পেজিনেশন এবং ক্যাশ সহ।
    """
    cache_params = {'marhala_id': marhala_id or 'all', 'page': page, 'page_size': page_size}
    cache_key = SubjectCache.generate_query_key(SubjectCache.SUBJECT_SETTINGS_LIST_KEY, cache_params)
    cached_data = SubjectCache.get_cache(cache_key)
    if cached_data:
        return cached_data, True

    settings_qs = SubjectSettings.objects.select_related('marhala', 'subject').only(
        'id', 'marhala_id', 'subject_id', 'marhala_type', 'subject_names',
        'student_type', 'syllabus_type', 'markaz_type', 'subject_type',
        'total_marks', 'pass_marks', 'status', 'subject_code',
        'marhala__id', 'marhala__marhala_name_bn',
        'subject__id', 'subject__subject_code'
    ).order_by('marhala_id', 'subject_code')

    if marhala_id:
        settings_qs = settings_qs.filter(marhala_id=marhala_id)

    total_count = settings_qs.count()
    start = (page - 1) * page_size
    end = start + page_size
    paginated = settings_qs[start:end]

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
    return response_data, False
