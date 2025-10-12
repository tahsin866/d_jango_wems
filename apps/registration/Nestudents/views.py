from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.core.cache import cache
from apps.registration.OldStudent.models import student_basic, student_adresss, student_attachment
from apps.users.models import UserInformation
from .serializers import NewStudentSerializer
import random

BEFAQ_BOARD_NAME = 'বেফাকুল মাদারিসিল আরাবিয়া বাংলাদেশ'

class NewStudentRegistrationView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

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

    def get_auto_markaz_id(self, madrasha_id):
        """Auto-derive markaz_id from madrasha_under_centers"""
        try:
            from apps.Markaz.models import MadrashaUnderCenter
            mapping = MadrashaUnderCenter.objects.filter(child_madrasha_id=str(madrasha_id)).first()
            if mapping and mapping.parent_madrasha_id:
                auto_markaz_id = int(mapping.parent_madrasha_id) if str(mapping.parent_madrasha_id).isdigit() else None
                print(f"🔥 Auto-derived markaz_id: {auto_markaz_id} from parent_madrasha_id: {mapping.parent_madrasha_id}")
                return auto_markaz_id
            else:
                print(f"⚠️ No markaz mapping found for madrasha_id: {madrasha_id}")
                return None
        except Exception as e:
            print(f"⚠️ Failed to auto-derive markaz_id: {e}")
            return None

    def get_auto_exam_id(self):
        """Get exam_id from ExamSetup table based on current year (like OldStudent)"""
        try:
            from apps.admin.CentralExam.models import ExamSetup
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
            
            exam_id = exam_setup.id if exam_setup else None
            print(f"🔥 Auto-derived exam_id: {exam_id} from ExamSetup")
            return exam_id
        except Exception as e:
            print(f"⚠️ Failed to auto-derive exam_id: {e}")
            return None

    def post(self, request):
        serializer = NewStudentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data

        # Auto-detect madrasha_id from user session (like OldStudent)
        user_madrasha_id = None
        auto_markaz_id = None
        auto_exam_id = None
        user_id = request.data.get('user_id') or request.data.get('user') or (request.user.id if hasattr(request, 'user') and request.user.is_authenticated else None)
        
        if user_id:
            user_madrasha_id = self.get_user_madrasha_id(user_id)
            if user_madrasha_id:
                print(f"🔥 Mapped madrasha_id from user_information: {user_madrasha_id} for user_id: {user_id}")
                auto_markaz_id = self.get_auto_markaz_id(user_madrasha_id)
            else:
                print(f"⚠️ Could not find madrasha_id for user_id: {user_id}")
                # Default fallback madrasha_id and markaz_id for testing
                user_madrasha_id = 1  # Default test madrasha
                auto_markaz_id = 1    # Default test markaz
        else:
            print("⚠️ No user_id provided in request - using default values")
            # Default fallback values for testing
            user_madrasha_id = 1  # Default test madrasha
            auto_markaz_id = 1    # Default test markaz
            
        # Auto-detect exam_id from ExamSetup table (like OldStudent)
        auto_exam_id = self.get_auto_exam_id()
        serializer = NewStudentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data

        # Determine students_type
        board_id = data.get('board_id')
        irregular_year = data.get('irregular_year')
        
        print(f"🔥 Board data received:")
        print(f"  board_id: {board_id}")
        print(f"  irregular_year: {irregular_year}")

        # Logic: if board_id is not 1 (main befaq) => students_type = 'অনিয়মিত (অন্যান্য)' else 'নিয়মিত'
        if board_id and board_id != 1:
            students_type_val = 'অনিয়মিত (অন্যান্য)'
        else:
            students_type_val = 'নিয়মিত'

        # Generate reg_no like OldStudent (6 digits: YY + 4 random)
        year_last2 = str(timezone.now().year)[-2:]
        reg_no = int(f"{year_last2}{random.randint(1000,9999)}")

        try:
            # Ensure irregular_sub numeric
            try:
                irregular_sub_val = int(data.get('irregular_sub')) if data.get('irregular_sub') not in [None, ''] else 0
            except Exception:
                irregular_sub_val = 0

            basic = student_basic.objects.create(
                student_name_bn=data.get('student_name_bn',''),
                student_name_ar=data.get('student_name_ar',''),
                student_name_en=data.get('student_name_en',''),
                father_name_bn=data.get('father_name_bn',''),
                father_name_ar=data.get('father_name_ar',''),
                father_name_en=data.get('father_name_en',''),
                mother_name_bn=data.get('mother_name_bn',''),
                mother_name_ar=data.get('mother_name_ar',''),
                mother_name_en=data.get('mother_name_en',''),
                date_of_birth=data.get('date_of_birth'),
                roll_no=0,
                reg_no=reg_no,
                year=timezone.now().year,
                status='pending',
                students_type=students_type_val,
                exam_id=auto_exam_id,
                mobile=data.get('mobile',''),
                # Auto-detected fields
                marhala_id=data.get('marhala_id'),
                madrasha_id=user_madrasha_id,
                markaz_id=auto_markaz_id,
                # New fields
                board_id=board_id,
                irregular_year=irregular_year or '',
                irregular_sub=irregular_sub_val,
                ip_address=request.META.get('REMOTE_ADDR','127.0.0.1'),
                created_at=timezone.now(),
                updated_at=timezone.now(),
                cid=data.get('cid'),
                srtype=data.get('srtype'),
                is_old=0,
            )
        except Exception as e:
            return Response({'error':'Failed to create student_basic','details':str(e)}, status=500)

        # Address
        try:
            print(f"🔥 Address data received:")
            print(f"  division_id: {data.get('division_id','')}")
            print(f"  district_id: {data.get('district_id','')}")
            print(f"  thana_id: {data.get('thana_id','')}")
            
            student_adresss.objects.update_or_create(
                id=basic.id,
                defaults={
                    'student_id': basic.id,
                    'division': data.get('division_id',''),
                    'district': data.get('district_id',''),
                    'thana': data.get('thana_id',''),
                    'post_office': '',
                    'passport_photo': data.get('passport_photo',''),
                    'birth_certificate_no': data.get('birth_no',''),
                    'birth_certificate_photo': data.get('birth_attach',''),
                    'nid_no': data.get('nid_no',''),
                    'nid_photo': data.get('nid_attach',''),
                }
            )
            print(f"✅ Address record created/updated for student_id: {basic.id}")
        except Exception as e:
            print(f"❌ Error creating address record: {e}")
            pass

        # Attachments
        try:
            # Handle file uploads properly
            student_image_file = data.get('student_image')
            marksheet_file = data.get('marksheet')
            
            attachment_data = {
                'student_id': basic.id,
                'birth_no': data.get('birth_no',''),
                'birth_attach': data.get('birth_attach',''),
                'nid_no': data.get('nid_no',''),
                'nid_attach': data.get('nid_attach',''),
                'marksheet': marksheet_file.name if marksheet_file and hasattr(marksheet_file, 'name') else '',
            }
            
            student_attachment.objects.update_or_create(
                id=basic.id,
                defaults=attachment_data
            )
        except Exception as e:
            print(f"Error creating attachment: {e}")
            pass

        return Response({
            'success': True,
            'student_id': basic.id,
            'reg_no': reg_no,
            'students_type': students_type_val,
            'board_id_saved': board_id,
            'irregular_year_saved': irregular_year,
            'madrasha_id': user_madrasha_id,
            'markaz_id': auto_markaz_id,
            'exam_id': auto_exam_id,
            'user_id_used': user_id,
        }, status=201)
