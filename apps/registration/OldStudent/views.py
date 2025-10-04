from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.cache import cache  # Fixed cache import
from .models import Student
from .models import Student
from .models import student_basic, student_adresss, student_attachment
from django.utils import timezone
import random
import uuid
import hashlib


class OldStudentRegistrationView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # Disable authentication for this view
    permission_classes = [AllowAny]
    
    def trim(self, val):
        return val[:255] if isinstance(val, str) and len(val) > 255 else val

    def post(self, request):
        # 🚀 REDIS CACHE SYSTEM: Check for session key first
        session_key = request.data.get('session_key')
        
        if session_key:
            # Retrieve search data from Redis cache using session key
            cached_data = cache.get(session_key)
            
            if not cached_data:
                return Response({
                    'error': 'Session expired or invalid. Please search again.',
                    'code': 'SESSION_EXPIRED'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Set search_result from cached Redis data
            search_result = cached_data
            
            # Optionally delete session after use (one-time use)
            # cache.delete(session_key)  # Uncomment for one-time use
            
        else:
            # Fallback mode: Direct search_result (for backward compatibility)
            search_result = request.data.get('search_result', {})
        
        # Production-safe validation
        has_session = bool(session_key)
        
        # Extract data from request
        personal = request.data.get('personal', {})
        address = request.data.get('address', {})
        attachments = request.data.get('attachments', {})

        # Map fields from search_result if available
        student_basic_data = search_result.get('student_basic', {}) if search_result else {}
        student_results_data = search_result.get('student_results', {}) if search_result else {}
        subjects = student_results_data.get('subjects', [])

        # Custom logic for reg_no, year, status, students_type, etc.
        year = str(timezone.now().year)[-2:]
        marhala_id_from_search = str(student_basic_data.get('marhala_id', ''))
        marhala_id_from_personal = str(personal.get('marhala_id', ''))
        marhala_id = marhala_id_from_search or marhala_id_from_personal
        
        # Validation
        has_valid_marhala = bool(marhala_id and marhala_id.isdigit())
        
        reg_code = str(random.randint(1000, 9999))
        reg_no = int(f"{year}{marhala_id}{reg_code}")

        status_val = personal.get('status', 'pending')

        # Field mappings as requested:
        # marhala_id, cid, srtype, students_type, exam_id in this file data will get from exam_setups tables
        # madrasha_id also come from students table

        # From student_basic.marhala_id -> set cid (since both are in same table)
        marhala_id_from_basic = student_basic_data.get('marhala_id', None)
        cid_val = student_basic_data.get('cid', None)  # Get cid directly from search result
        if not cid_val and marhala_id_from_basic:
            cid_val = int(marhala_id_from_basic) if str(marhala_id_from_basic).isdigit() else None
        elif not cid_val:
            cid_val = int(marhala_id) if marhala_id and marhala_id.isdigit() else None

        # From student_results.srtype -> set students_type (as requested)
        srtype_from_results = student_results_data.get('srtype', None)
        srtype_from_basic = student_basic_data.get('srtype', None)  # Direct from search result
        
        # Use srtype from basic first, then results
        srtype_val = None
        if srtype_from_basic is not None:
            srtype_val = int(srtype_from_basic) if str(srtype_from_basic).isdigit() else None
        elif srtype_from_results is not None:
            srtype_val = int(srtype_from_results) if str(srtype_from_results).isdigit() else None

        # students_type from personal, student_basic_data, or first subject's result_type
        students_type_val = personal.get('students_type')
        if not students_type_val:
            students_type_val = student_basic_data.get('students_type')
        if not students_type_val and subjects:
            students_type_val = subjects[0].get('result_type', '')
        if not students_type_val:
            students_type_val = ''

        # exam_id = fetch from exam_setups table based on current year (as requested)
        # Priority: personal.exam_id > current year exam_setup
        exam_id_val = personal.get('exam_id', None)
        
        # Convert to int if it's a string
        if exam_id_val and str(exam_id_val).isdigit():
            exam_id_val = int(exam_id_val)
        
        if not exam_id_val:
            try:
                from apps.admin.CentralExam.models import ExamSetup
                # Get current exam setup based on year - multiple strategies
                current_year = timezone.now().year
                
                # Strategy 1: Exact match with current year
                exam_setup = ExamSetup.objects.filter(
                    english_year=str(current_year)
                ).first()
                
                # Strategy 2: If no exact match, try contains
                if not exam_setup:
                    exam_setup = ExamSetup.objects.filter(
                        english_year__contains=str(current_year)
                    ).first()
                
                # Strategy 3: If still no match, get the latest one
                if not exam_setup:
                    exam_setup = ExamSetup.objects.order_by('-created_at').first()
                
                exam_id_val = exam_setup.id if exam_setup else None
            except Exception as e:
                exam_id_val = None

        # madrasha_id = mid from student_results and also from student_basic (from Student table)
        mid_from_results = student_results_data.get('mid', None)
        mid_from_basic = student_basic_data.get('madrasha_id', None)  # From Student table via search result
        madrasha_id_val = None

        # Priority: student_basic (from Student table) > student_results
        if mid_from_basic:
            madrasha_id_val = int(mid_from_basic) if str(mid_from_basic).isdigit() else None
        elif mid_from_results:
            madrasha_id_val = int(mid_from_results) if str(mid_from_results).isdigit() else None

        # Field mapping validation
        has_basic_data = bool(student_basic_data)
        has_results_data = bool(student_results_data)

        try:
            # Get IP address with proper validation
            ip_address_val = personal.get('ip_address')
            if not ip_address_val or ip_address_val.strip() == '':
                ip_address_val = '127.0.0.1'

            # Parse datetime fields
            created_at_val = timezone.now()
            updated_at_val = timezone.now()
            
            # Try to parse from personal data if provided
            if personal.get('created_at'):
                try:
                    from django.utils.dateparse import parse_datetime
                    parsed_dt = parse_datetime(personal.get('created_at'))
                    if parsed_dt:
                        created_at_val = parsed_dt
                except:
                    pass
            
            if personal.get('updated_at'):
                try:
                    from django.utils.dateparse import parse_datetime
                    parsed_dt = parse_datetime(personal.get('updated_at'))
                    if parsed_dt:
                        updated_at_val = parsed_dt
                except:
                    pass

            # Insert into student_basic
            basic = student_basic.objects.create(
                student_name_bn=personal.get('student_name_bn', student_basic_data.get('student_name_bn', '')),
                student_name_ar=personal.get('student_name_ar', ''),
                student_name_en=personal.get('student_name_en', ''),
                father_name_bn=personal.get('father_name_bn', student_basic_data.get('father_name_bn', '')),
                father_name_ar=personal.get('father_name_ar', ''),
                father_name_en=personal.get('father_name_en', ''),
                mother_name_bn=personal.get('mother_name_bn', student_basic_data.get('mother_name_bn', '')),
                mother_name_ar=personal.get('mother_name_ar', ''),
                mother_name_en=personal.get('mother_name_en', ''),
                date_of_birth=personal.get('date_of_birth', student_basic_data.get('date_of_birth', None)),
                roll_no=0,  # Set to 0 instead of None to avoid database constraint issues
                reg_no=reg_no,
                year=timezone.now().year,
                status=status_val,
                students_type=students_type_val or '',  # CharField - string
                exam_id=exam_id_val,  # IntegerField - int or None
                madrasha_id=int(personal.get('madrasha_id')) if personal.get('madrasha_id') and str(personal.get('madrasha_id')).isdigit() else madrasha_id_val,  # From personal payload
                markaz_id=None,  # IntegerField - None
                irregular_sub=personal.get('irregular_sub', ''),
                marhala_id=int(personal.get('marhala_id')) if personal.get('marhala_id') and str(personal.get('marhala_id')).isdigit() else (int(marhala_id) if marhala_id and marhala_id.isdigit() else None),  # Enhanced fallback logic
                mobile=personal.get('mobile', ''),  # CharField - string from personal payload
                ip_address=personal.get('ip_address', '127.0.0.1'),  # From personal payload
                created_at=created_at_val,  # DateTimeField - datetime object
                updated_at=updated_at_val,  # DateTimeField - datetime object
                cid=int(personal.get('cid')) if personal.get('cid') and str(personal.get('cid')).isdigit() else cid_val,  # From personal payload
                srtype=int(personal.get('srtype')) if personal.get('srtype') and str(personal.get('srtype')).isdigit() else srtype_val,  # From personal payload
                is_old=1  # IntegerField - int
            )
        except Exception as e:
            # Log error without exposing sensitive data
            raise
        
        # Registration completed successfully

        # Insert into student_adresss
        student_adresss.objects.create(
            id=basic.id,
            student_id=basic.id,
            division=self.trim(address.get('division', '')),
            district=self.trim(address.get('district', '')),
            thana=self.trim(address.get('thana', '')),
            post_office=self.trim(address.get('post_office', '')),
            passport_photo=self.trim(address.get('passport_photo', '')),
            birth_certificate_no=self.trim(address.get('birth_certificate_no', '')),
            birth_certificate_photo=self.trim(address.get('birth_certificate_photo', '')),
            nid_no=self.trim(address.get('nid_no', '')),
            nid_photo=self.trim(address.get('nid_photo', ''))
        )

        # Insert into student_attachment
        student_attachment.objects.create(
            id=basic.id,
            student_id=basic.id,
            birth_no=self.trim(attachments.get('birth_no', '')),
            birth_attach=self.trim(attachments.get('birth_attach', '')),
            nid_no=self.trim(attachments.get('nid_no', '')),
            nid_attach=self.trim(attachments.get('nid_attach', ''))
        )

        return Response({'success': True, 'student_id': basic.id, 'reg_no': reg_no}, status=status.HTTP_201_CREATED)

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
            # Hide roll_no in response but keep in cache for registration
            response_cached_data = cached_data.copy()
            if 'student_basic' in response_cached_data and 'roll_no' in response_cached_data['student_basic']:
                response_cached_data['student_basic']['roll_no'] = ''
            return Response(response_cached_data, status=status.HTTP_200_OK)

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
        irregular_subjects = []
        # Find latest year in Student table
        try:
            latest_year = Student.objects.order_by('-years').values_list('years', flat=True).first()
        except Exception:
            latest_year = None
        # If requested year < latest_year, force all subjects to irregular
        force_irregular = latest_year and year < latest_year
        for i in range(1, 12):
            label = getattr(student, f'sublabel_{i}', None)
            value = getattr(student, f'subvalue_{i}', None)
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
            if force_irregular:
                result_type_sub = 'অনিয়মিত (অন্যান্য)'
                irregular_subjects.append(label)
            elif fail_cond and (is_rasib or is_absent or is_jobt):
                result_type_sub = 'অনিয়মিত (অন্যান্য)'
                irregular_subjects.append(label)
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
        has_jobt = any(s.get('division') == 'যব্ত' and s.get('absence') == '1' for s in subjects)
        found_irregular = any(s.get('result_type', '').startswith('অনিয়মিত') for s in subjects)
        # মানোউন্নয়ন লজিক: division যদি 'জায়্যিদ', 'জায়্যিদ জিদ্দান', 'মাকবুল' হয়
        is_manounnoyon = False
        if header_marhala_id == '9' and marhala == '2':
            for s in subjects:
                if s.get('division') in ['জায়্যিদ', 'জায়্যিদ জিদ্দান', 'মাকবুল']:
                    s['result_type'] = 'মানোউন্নয়ন'
                    is_manounnoyon = True
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
            'srtype': student.srtype,
            'class_name': student.class_name,
            'markaj': student.markaj,
            'marid': student.marid,
            'melhaq': student.melhaq,
            'subjects': subjects,
            'irregular_subjects': irregular_subjects
        }

        data = {
            'student_basic': {
                'student_name_bn': student.name,
                'father_name_bn': student.father,
                'mother_name_bn': '',
                'date_of_birth': student.dateofbirth,
                'roll_no': student.roll,  # Keep actual roll_no for cache/registration
                'reg_no': student.reg_id,
                'marhala_id': student.marhala_id,
                'year': student.years,
                'cid': student.cid,  # Include cid from Student table
                'srtype': student.srtype,  # Include srtype from Student table
                'madrasha_id': student.mid,  # Include madrasha_id from Student table
                'mobile': student.mobile,  # Include mobile from Student table
            },
            'student_results': grouped_result
        }

        cache.set(cache_key, data, timeout=60*60*24)
        
        # 🚀 REDIS CACHE SYSTEM: Generate unique session key for search result
        import secrets
        session_key = f"student_search_{secrets.token_urlsafe(16)}_{timezone.now().timestamp()}"
        
        # Store search data in Redis cache with session key (2 hours expiry)
        cache.set(session_key, data, timeout=60*60*2)  # 2 hours expiry
        
        # Return optimized response with session key (hide roll_no in response)
        response_data = {
            'student_basic': {
                **data['student_basic'],
                'roll_no': ''  # Hide roll_no in frontend response
            },
            'student_results': {
                'madrasha': grouped_result['madrasha'],
                'class_name': grouped_result['class_name'],
                'markaz': grouped_result['markaj'],
                'subjects': grouped_result['subjects'],
                'irregular_subjects': grouped_result['irregular_subjects']
            },
            'session_key': session_key
        }
        
        response = Response(response_data, status=status.HTTP_200_OK)
        
        return response