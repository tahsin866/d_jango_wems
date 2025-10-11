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
from apps.users.models import User, UserInformation
import random
import uuid
import hashlib


class OldStudentRegistrationView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # Disable authentication for this view
    permission_classes = [AllowAny]
    
    def trim(self, val):
        return val[:255] if isinstance(val, str) and len(val) > 255 else val

    def get_user_madrasha_id(self, user_id):
        """Get madrasha_id from user_information table using user_id"""
        try:
            user_info = UserInformation.objects.get(user_id=user_id)
            return user_info.madrasha_id
        except UserInformation.DoesNotExist:
            return None
        except Exception as e:
            print(f"Error getting user madrasha_id: {str(e)}")
            return None

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

        # 🔥 NEW LOGIC: Get user_id and map marhala_id from user_information table
        user_id = request.data.get('user_id')
        user_madrasha_id = None
        auto_markaz_id = None

        if user_id:
            user_madrasha_id = self.get_user_madrasha_id(user_id)
            if user_madrasha_id:
                print(f"🔥 Mapped madrasha_id from user_information: {user_madrasha_id} for user_id: {user_id}")
                
                # 🔥 AUTO-DERIVE markaz_id from madrasha_under_centers
                try:
                    from apps.Markaz.models import MadrashaUnderCenter
                    mapping = MadrashaUnderCenter.objects.filter(child_madrasha_id=str(user_madrasha_id)).first()
                    if mapping and mapping.parent_madrasha_id:
                        auto_markaz_id = int(mapping.parent_madrasha_id) if str(mapping.parent_madrasha_id).isdigit() else None
                        print(f"🔥 Auto-derived markaz_id: {auto_markaz_id} from parent_madrasha_id: {mapping.parent_madrasha_id}")
                    else:
                        print(f"⚠️ No markaz mapping found for madrasha_id: {user_madrasha_id}")
                except Exception as e:
                    print(f"⚠️ Failed to auto-derive markaz_id: {e}")
            else:
                print(f"⚠️ Could not find madrasha_id for user_id: {user_id}")
        else:
            print("⚠️ No user_id provided in request")

        # Map fields from search_result if available
        student_basic_data = search_result.get('student_basic', {}) if search_result else {}
        student_results_data = search_result.get('student_results', {}) if search_result else {}
        subjects = student_results_data.get('subjects', [])

        # Custom logic for reg_no, year, status, students_type, etc.
        year = str(timezone.now().year)[-2:]

        # 🔥 FIXED: marhala_id comes from search_result/personal (NOT from user_information)
        marhala_id_from_search = str(student_basic_data.get('marhala_id', ''))
        marhala_id_from_personal = str(personal.get('marhala_id', ''))

        # Priority order: search_result > personal (original logic)
        marhala_id = marhala_id_from_search or marhala_id_from_personal

        # 🔥 CORRECT: madrasha_id comes from user_information table
        madrasha_id_from_user = user_madrasha_id if user_madrasha_id else None

        # Validation
        has_valid_marhala = bool(marhala_id and marhala_id.isdigit())
        
        # 🔥 FIXED: Generate 6-digit registration number
        # Simple and robust approach: year (2) + random 4 digits = 6 digits total
        year_last2 = str(timezone.now().year)[-2:]  # Last 2 digits of year
        random_4digits = str(random.randint(1000, 9999))  # 4-digit random number
        reg_no = int(f"{year_last2}{random_4digits}")  # Guaranteed 6 digits

        print(f"✅ Generated 6-digit reg_no: {reg_no} (year: {year_last2}, random: {random_4digits})")

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

            # Check for existing student to avoid duplicate key errors
            # Use reg_no and marhala_id as unique identifiers for existing students
            existing_student = None
            if reg_no and marhala_id:
                try:
                    existing_student = student_basic.objects.get(
                        reg_no=reg_no,
                        marhala_id=int(marhala_id) if marhala_id and marhala_id.isdigit() else None
                    )
                except student_basic.DoesNotExist:
                    existing_student = None
                except Exception as e:
                    # Handle any other database errors gracefully
                    existing_student = None

            # Prepare student data
            student_data = {
                'student_name_bn': personal.get('student_name_bn', student_basic_data.get('student_name_bn', '')),
                'student_name_ar': personal.get('student_name_ar', ''),
                'student_name_en': personal.get('student_name_en', ''),
                'father_name_bn': personal.get('father_name_bn', student_basic_data.get('father_name_bn', '')),
                'father_name_ar': personal.get('father_name_ar', ''),
                'father_name_en': personal.get('father_name_en', ''),
                'mother_name_bn': personal.get('mother_name_bn', student_basic_data.get('mother_name_bn', '')),
                'mother_name_ar': personal.get('mother_name_ar', ''),
                'mother_name_en': personal.get('mother_name_en', ''),
                'date_of_birth': personal.get('date_of_birth', student_basic_data.get('date_of_birth', None)),
                'roll_no': 0,  # Set to 0 instead of None to avoid database constraint issues
                'reg_no': reg_no,
                'year': timezone.now().year,
                'status': status_val,
                'students_type': students_type_val or '',  # CharField - string
                'exam_id': exam_id_val,  # IntegerField - int or None
                'madrasha_id': madrasha_id_from_user if madrasha_id_from_user else (int(personal.get('madrasha_id')) if personal.get('madrasha_id') and str(personal.get('madrasha_id')).isdigit() else madrasha_id_val),  # 🔥 FIXED: user_information > personal > search_result
                'markaz_id': auto_markaz_id if auto_markaz_id else (int(personal.get('markaz_id')) if personal.get('markaz_id') and str(personal.get('markaz_id')).isdigit() else None),  # 🔥 NEW: Auto-derived markaz_id from madrasha_under_centers
                'irregular_sub': personal.get('irregular_sub', ''),
                'marhala_id': int(personal.get('marhala_id')) if personal.get('marhala_id') and str(personal.get('marhala_id')).isdigit() else (int(marhala_id) if marhala_id and marhala_id.isdigit() else None),  # 🔥 FIXED: From search_result/personal (NOT user_information)
                'mobile': personal.get('mobile', ''),  # CharField - string from personal payload
                'ip_address': personal.get('ip_address', '127.0.0.1'),  # From personal payload
                'created_at': created_at_val,  # DateTimeField - datetime object
                'updated_at': updated_at_val,  # DateTimeField - datetime object
                'cid': int(personal.get('cid')) if personal.get('cid') and str(personal.get('cid')).isdigit() else cid_val,  # From personal payload
                'srtype': int(personal.get('srtype')) if personal.get('srtype') and str(personal.get('srtype')).isdigit() else srtype_val,  # From personal payload
                'is_old': 1  # IntegerField - int
            }

            # Insert or update student_basic
            if existing_student:
                # Update existing student
                for key, value in student_data.items():
                    setattr(existing_student, key, value)
                existing_student.save()
                basic = existing_student
            else:
                # Create new student
                basic = student_basic.objects.create(**student_data)

        except Exception as e:
            # Log error with more details for debugging
            error_msg = f"Student registration error: {str(e)}"
            print(f"ERROR: {error_msg}")
            print(f"reg_no: {reg_no}, marhala_id: {marhala_id}")

            # 🔥 ENHANCED ERROR HANDLING
            if "duplicate key" in str(e).lower():
                return Response({
                    'error': 'Student with this registration number already exists.',
                    'code': 'DUPLICATE_REGISTRATION',
                    'reg_no': reg_no
                }, status=status.HTTP_409_CONFLICT)
            elif "integer out of range" in str(e).lower():
                return Response({
                    'error': f'Registration number {reg_no} is too large. Please try again.',
                    'code': 'REG_NO_OUT_OF_RANGE',
                    'reg_no': reg_no,
                    'details': 'The generated registration number exceeds the maximum allowed value. The system will generate a new one.'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'error': 'Registration failed. Please try again.',
                    'code': 'REGISTRATION_ERROR',
                    'details': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Registration completed successfully

        # Insert into student_adresss with error handling
        try:
            student_adresss.objects.update_or_create(
                id=basic.id,
                defaults={
                    'student_id': basic.id,
                    'division': self.trim(address.get('division', '')),
                    'district': self.trim(address.get('district', '')),
                    'thana': self.trim(address.get('thana', '')),
                    'post_office': self.trim(address.get('post_office', '')),
                    'passport_photo': self.trim(address.get('passport_photo', '')),
                    'birth_certificate_no': self.trim(address.get('birth_certificate_no', '')),
                    'birth_certificate_photo': self.trim(address.get('birth_certificate_photo', '')),
                    'nid_no': self.trim(address.get('nid_no', '')),
                    'nid_photo': self.trim(address.get('nid_photo', ''))
                }
            )
        except Exception as e:
            print(f"Warning: Failed to create student address record: {str(e)}")
            # Continue with registration even if address creation fails

        # Insert into student_attachment with error handling
        try:
            student_attachment.objects.update_or_create(
                id=basic.id,
                defaults={
                    'student_id': basic.id,
                    'birth_no': self.trim(attachments.get('birth_no', '')),
                    'birth_attach': self.trim(attachments.get('birth_attach', '')),
                    'nid_no': self.trim(attachments.get('nid_no', '')),
                    'nid_attach': self.trim(attachments.get('nid_attach', ''))
                }
            )
        except Exception as e:
            print(f"Warning: Failed to create student attachment record: {str(e)}")
            # Continue with registration even if attachment creation fails

        # Determine response message based on whether student was updated or created
        action = "updated" if existing_student else "registered"
        message = f"Student {action} successfully!"

        # Add info about field mapping for debugging
        response_data = {
            'success': True,
            'student_id': basic.id,
            'reg_no': reg_no,
            'action': action,
            'message': message,
            'marhala_id': basic.marhala_id,
            'marhala_id_source': 'search_result_or_form',
            'madrasha_id': basic.madrasha_id,
            'madrasha_id_source': 'user_information' if madrasha_id_from_user else 'search_result_or_form',
            'markaz_id': basic.markaz_id,
            'markaz_id_source': 'auto_derived_from_madrasha_under_centers' if auto_markaz_id else 'manual_or_none'
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

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