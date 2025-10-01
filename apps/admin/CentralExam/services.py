# services.py
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.cache import cache
import json

from .models import ExamSetup
from apps.admin.CentralExam.models import ExamFee
from .serializers import ExamSetupSerializer, ExamFeeSerializer


def get_exam_setup_list():
    cache_key = "exam_setup_list"
    data = cache.get(cache_key)

    if data is None:
        exam_setups = ExamSetup.objects.all()
        serializer = ExamSetupSerializer(exam_setups, many=True)
        data = serializer.data
        cache.set(cache_key, json.dumps(data), timeout=60*30)
    else:
        data = json.loads(data)
    return data


def get_exam_setup_detail(pk):
    cache_key = f"exam_setup_{pk}"
    data = cache.get(cache_key)

    if data is None:
        exam_setup = get_object_or_404(ExamSetup, pk=pk)
        serializer = ExamSetupSerializer(exam_setup)
        data = serializer.data
        cache.set(cache_key, json.dumps(data), timeout=60*30)
    else:
        data = json.loads(data)
    return data


def list_exam_fees_by_setup(exam_setup_id):
    return ExamFee.objects.filter(exam_setup_id=exam_setup_id).select_related('marhala', 'exam_setup')


def get_exam_fee_detail(fee_id):
    return ExamFee.objects.select_related('marhala', 'exam_setup').get(id=fee_id)


def update_exam_fee(fee_id, data):
    exam_fee = ExamFee.objects.get(id=fee_id)
    serializer = ExamFeeSerializer(exam_fee, data=data, partial=True)
    if serializer.is_valid():
        with transaction.atomic():
            updated_fee = serializer.save()
        return updated_fee, None
    return None, serializer.errors


def bulk_create_fees(fees):
    created_fees, errors = [], []
    latest_exam = ExamSetup.objects.order_by('-id').first()
    if not latest_exam:
        return None, [{'exam_setup': ['কোনো কেন্দ্রীয় পরীক্ষা পাওয়া যায়নি']}]

    for idx, fee_data in enumerate(fees):
        if not fee_data.get('exam_setup'):
            fee_data['exam_setup'] = latest_exam.id

        serializer = ExamFeeSerializer(data=fee_data)
        if not serializer.is_valid():
            errors.append({'index': idx, 'errors': serializer.errors, 'item_data': fee_data})
            continue

        try:
            with transaction.atomic():
                created_fee = serializer.save()
                created_fees.append(ExamFeeSerializer(created_fee).data)
        except Exception as e:
            errors.append({'index': idx, 'errors': {'database_error': [str(e)]}, 'item_data': fee_data})

    return created_fees, errors


def create_exam_setup(data):
    serializer = ExamSetupSerializer(data=data)
    if serializer.is_valid():
        with transaction.atomic():
            exam_setup = serializer.save()
        return exam_setup, None
    return None, serializer.errors


def list_exam_setups(search_query="", year_filter="", exam_name_filter=""):
    exam_setups = ExamSetup.objects.all()
    if search_query:
        exam_setups = exam_setups.filter(
            Q(exam_name__icontains=search_query) |
            Q(arabic_year__icontains=search_query) |
            Q(bangla_year__icontains=search_query) |
            Q(english_year__icontains=search_query)
        )
    if year_filter:
        exam_setups = exam_setups.filter(
            Q(arabic_year=year_filter) |
            Q(bangla_year=year_filter) |
            Q(english_year=year_filter)
        )
    if exam_name_filter:
        exam_setups = exam_setups.filter(exam_name=exam_name_filter)

    exam_setups = exam_setups.order_by('-created_at')
    return exam_setups


def get_exam_setup(exam_id):
    return ExamSetup.objects.get(id=exam_id)


def update_exam_setup(exam_id, data):
    exam_setup = ExamSetup.objects.get(id=exam_id)
    serializer = ExamSetupSerializer(exam_setup, data=data, partial=True)
    if serializer.is_valid():
        with transaction.atomic():
            updated = serializer.save()
        return updated, None
    return None, serializer.errors


def delete_exam_setup(exam_id):
    exam_setup = ExamSetup.objects.get(id=exam_id)
    exam_setup.delete()
    return True


def get_latest_exam_setup():
    return ExamSetup.objects.order_by('-id').first()
