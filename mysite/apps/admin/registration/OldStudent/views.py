from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.cache import cache  # Django Redis cache
from .models import student_basic, student_results

class OldStudentSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        year_str = request.GET.get('year')
        roll_no = request.GET.get('roll')
        reg_no = request.GET.get('registration')
        marhala_id = request.GET.get('marhalaId')

        # Extract English year from formatted string
        try:
            year = int(year_str.split('/')[-1].replace('ঈসাব্দ', '').strip()) if year_str else None
        except Exception:
            return Response({'error': 'Invalid year format.'}, status=status.HTTP_400_BAD_REQUEST)

        if not all([year, roll_no, reg_no, marhala_id]):
            return Response({'error': 'year, roll_no, reg_no, and marhalaId are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Redis cache key (unique per student)
        cache_key = f"student_data:{year}:{roll_no}:{reg_no}:{marhala_id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        # Fetch student_basic from DB
        student = get_object_or_404(
            student_basic,
            year=year,
            roll_no=roll_no,
            reg_no=reg_no,
            marhala_id=marhala_id
        )

        # Fetch related student_results from DB
        results_qs = student_results.objects.filter(student_id=student.id).only(
            'id', 'student_id', 'madrasha', 'mid', 'class_name',
            'markaj', 'marid', 'melhaq', 'subject_label', 'subject_value',
            'total', 'grace_label', 'grace_value', 'positions', 'division',
            'absence', 'possub', 'created_at', 'updated_at'
        )

        results_raw = list(results_qs.values(
            'id', 'student_id', 'madrasha', 'mid', 'class_name',
            'markaj', 'marid', 'melhaq', 'subject_label', 'subject_value',
            'total', 'grace_label', 'grace_value', 'positions', 'division',
            'absence', 'possub', 'created_at', 'updated_at'
        ))

        # Determine irregular logic and group results
        threshold = 33 if student.year >= 2024 else 35
        below_threshold_count = 0
        zero_count = 0
        absent_count = 0
        subjects = []
        # Use first result for common info
        common_fields = ['madrasha', 'mid', 'class_name', 'markaj', 'marid', 'melhaq']
        common_info = {k: results_raw[0][k] if results_raw else '' for k in common_fields}

        for r in results_raw:
            try:
                subject_val = float(r.get('subject_value', 0))
            except (TypeError, ValueError):
                subject_val = 0
            # absence=অনুপস্থিত যদি subject_value=0
            if subject_val == 0:
                zero_count += 1
                r['absence'] = r.get('absence') or 'অনুপস্থিত'
            if subject_val < threshold:
                below_threshold_count += 1
            if r.get('absence') == 'অনুপস্থিত':
                absent_count += 1
            subjects.append({
                'label': r.get('subject_label'),
                'value': r.get('subject_value'),
                'absence': r.get('absence'),
                'division': r.get('division'),
                'result_type': None,  # will set below
            })

        # Determine irregular type
        result_type = 'নিয়মিত'
        if (zero_count + below_threshold_count) in [1,2] and (
            any(r.get('division') == 'রাসিব' for r in results_raw) or absent_count > 0):
            result_type = 'অনিয়মিত (যেমনই)'
        elif (zero_count + below_threshold_count) >= 3 or (zero_count == 1 and below_threshold_count > 1):
            result_type = 'অনিয়মিত (অন্যান্য)'

        # Set result_type for all subjects
        for s in subjects:
            s['result_type'] = result_type

        grouped_result = {
            **common_info,
            'subjects': subjects
        }

        data = {
            'student_basic': {
                'student_name_bn': student.student_name_bn,
                'father_name_bn': student.father_name_bn,
                'mother_name_bn': student.mother_name_bn,
                'date_of_birth': student.date_of_birth,
                'roll_no': student.roll_no,
                'reg_no': student.reg_no,
                'marhala_id': student.marhala_id,
                'year': student.year,
            },
            'student_results': grouped_result
        }

        # Save to Redis cache (expire after 24 hours)
        cache.set(cache_key, data, timeout=60*60*24)

        return Response(data, status=status.HTTP_200_OK)
