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
        # Extra logic: If header marhala_id==9 and cid==3, block result
        header_marhala_id = request.GET.get('marhalaId')
        marhala = request.GET.get('marhala')
        block_irregular_for_fazilat = False
        if header_marhala_id == '9' and marhala == '3':
            block_irregular_for_fazilat = True

        year_str = request.GET.get('year')
        roll_no = request.GET.get('roll')
        reg_no = request.GET.get('registration')

        # Extract English year from formatted string
        try:
            year = int(year_str.split('/')[-1].replace('ঈসাব্দ', '').strip()) if year_str else None
        except Exception:
            return Response({'error': 'Invalid year format.'}, status=status.HTTP_400_BAD_REQUEST)

        if not all([year, roll_no, reg_no, marhala]):
            return Response({'error': 'year, roll_no, reg_no, and marhala are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Redis cache key (unique per student)
        cache_key = f"student_data:{year}:{roll_no}:{reg_no}:{marhala}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        # Fetch student_basic from DB
        student = get_object_or_404(
            student_basic,
            year=year,
            roll_no=roll_no,
            reg_no=reg_no,
            cid=marhala  # এখন cid দিয়ে সার্চ হবে
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

            # subject-wise result_type
            result_type_sub = 'নিয়মিত'
            # ফেল কন্ডিশন
            fail_cond = subject_val < threshold
            # division/absence irregular
            is_rasib = r.get('division') == 'রাসিব'
            is_absent = r.get('absence') == 'অনুপস্থিত'
            is_jobt = r.get('division') == 'যব্ত' and r.get('absence') == 'যব্ত'
            if fail_cond and (is_rasib or is_absent or is_jobt):
                result_type_sub = 'অনিয়মিত (অন্যান্য)'
            subjects.append({
                'label': r.get('subject_label'),
                'value': r.get('subject_value'),
                'absence': r.get('absence'),
                'division': r.get('division'),
                'result_type': result_type_sub,
            })

        # Determine overall irregular type (for eligibility block)
        result_type = 'নিয়মিত'
        has_rasib = any(s.get('division') == 'রাসিব' for s in subjects)
        has_absent = any(s.get('absence') == 'অনুপস্থিত' for s in subjects)
        has_jobt = any(s.get('division') == 'যব্ত' and s.get('absence') == 'যব্ত' for s in subjects)
        found_irregular = any(s.get('result_type', '').startswith('অনিয়মিত') for s in subjects)
        if (zero_count + below_threshold_count) in [1,2] and (has_rasib or has_absent or has_jobt):
            result_type = 'অনিয়মিত (যেমনি)'
        elif ((zero_count + below_threshold_count) >= 3 or (zero_count == 1 and below_threshold_count > 1)):
            if has_rasib or has_absent or has_jobt:
                result_type = 'অনিয়মিত (অন্যান্য)'
            else:
                result_type = 'নিয়মিত'

            # Eligibility: marhala=3 এবং marhalaId=9 হলে, subjects-এ result_type 'অনিয়মিত' (যেমনই/অন্যান্য) অথবা division=='রাসিব' অথবা absence=='অনুপস্থিত' পাওয়া গেলে error response
            if header_marhala_id == '9' and marhala == '3':
                for s in subjects:
                    s['result_type'] = result_type if result_type == 'নিয়মিত' else 'অনিয়মিত (অন্যান্য)'
                found_rasib = any(s.get('division') == 'রাসিব' for s in subjects)
                found_absent = any(s.get('absence') == 'অনুপস্থিত' for s in subjects)
                found_irregular = any(s.get('result_type', '').startswith('অনিয়মিত') for s in subjects)
                if found_rasib or found_absent or found_irregular:
                    return Response({'error': 'আপনি ফযিলত মারহালায় পরীক্ষাদেওয়ার জন্য উপযুক্ত নন'}, status=status.HTTP_400_BAD_REQUEST)
            else:
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
