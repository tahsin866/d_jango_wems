from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.cache import cache  # Django Redis cache
from .models import Student

class OldStudentSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        header_marhala_id = request.GET.get('marhalaId')
        marhala = request.GET.get('marhala')
        year_str = request.GET.get('year')
        roll_no = request.GET.get('roll')
        reg_no = request.GET.get('registration')

        try:
            year = int(year_str.split('/')[-1].replace('ঈসাব্দ', '').strip()) if year_str else None
        except Exception:
            return Response({'error': 'Invalid year format.'}, status=status.HTTP_400_BAD_REQUEST)

        if not all([year, roll_no, reg_no, marhala]):
            return Response({'error': 'year, roll_no, reg_no, and marhala are required.'}, status=status.HTTP_400_BAD_REQUEST)

        cache_key = f"student_data:{year}:{roll_no}:{reg_no}:{marhala}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        # Fetch student from Student table
        student = get_object_or_404(
            Student,
            years=year,
            roll=roll_no,
            reg_id=reg_no,
            cid=marhala
        )

        # Gather subject results from Student fields
        subjects = []
        threshold = 33 if student.years >= 2024 else 35
        below_threshold_count = 0
        zero_count = 0
        absent_count = 0
        for i in range(1, 12):
            label = getattr(student, f'sublabel_{i}', None)
            value = getattr(student, f'subvalue_{i}', None)
            # শুধু label এবং value থাকলে subject list-এ যোগ হবে
            if not label or value is None or value == '':
                continue
            try:
                subject_val = float(value)
            except (TypeError, ValueError):
                subject_val = 0
            absence = 'অনুপস্থিত' if subject_val == 0 else ''
            division = getattr(student, 'division', '')
            if subject_val == 0:
                zero_count += 1
            if subject_val < threshold:
                below_threshold_count += 1
            if absence == 'অনুপস্থিত':
                absent_count += 1
            result_type_sub = 'নিয়মিত'
            fail_cond = subject_val < threshold
            is_rasib = division == 'রাসিব'
            is_absent = absence == 'অনুপস্থিত'
            is_jobt = division == 'যব্ত' and absence == 'যব্ত'
            if fail_cond and (is_rasib or is_absent or is_jobt):
                result_type_sub = 'অনিয়মিত (অন্যান্য)'
            subjects.append({
                'label': label,
                'value': value,
                'absence': absence,
                'division': division,
                'result_type': result_type_sub,
            })

        # Determine overall irregular type
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
            'madrasha': student.madrasha,
            'mid': student.mid,
            'class_name': student.class_name,
            'markaj': student.markaj,
            'marid': student.marid,
            'melhaq': student.melhaq,
            'subjects': subjects
        }

        data = {
            'student_basic': {
                'student_name_bn': student.name,
                'father_name_bn': student.father,
                'mother_name_bn': '',
                'date_of_birth': student.dateofbirth,
                'roll_no': student.roll,
                'reg_no': student.reg_id,
                'marhala_id': student.marhala_id,
                'year': student.years,
            },
            'student_results': grouped_result
        }

        cache.set(cache_key, data, timeout=60*60*24)
        return Response(data, status=status.HTTP_200_OK)
