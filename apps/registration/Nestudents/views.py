from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.core.cache import cache
from apps.registration.OldStudent.models import student_basic, student_adresss, student_attachment
from .serializers import NewStudentSerializer
import random

BEFAQ_BOARD_NAME = 'বেফাকুল মাদারিসিল আরাবিয়া বাংলাদেশ'

class NewStudentRegistrationView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = NewStudentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data

        # Determine students_type
        board_id = data.get('board_id')
        board_name = request.data.get('board_name')  # optional if provided
        irregular_year = data.get('irregular_year')

        # Logic: if board_name is not main befaq => students_type = 'অনিয়মিত (অন্যান্য)' else 'নিয়মিত'
        if board_name and board_name != BEFAQ_BOARD_NAME:
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
                exam_id=data.get('exam_id'),
                madrasha_id=data.get('madrasha_id'),
                markaz_id=data.get('markaz_id'),
                irregular_sub=irregular_sub_val,
                marhala_id=data.get('marhala_id'),
                mobile=data.get('mobile',''),
                ip_address=request.META.get('REMOTE_ADDR','127.0.0.1'),
                created_at=timezone.now(),
                updated_at=timezone.now(),
                cid=data.get('cid'),
                srtype=data.get('srtype'),
                is_old=0,
                board_id=board_id,
                irregular_year=irregular_year,
            )
        except Exception as e:
            return Response({'error':'Failed to create student_basic','details':str(e)}, status=500)

        # Address
        try:
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
        except Exception:
            pass

        # Attachments
        try:
            student_attachment.objects.update_or_create(
                id=basic.id,
                defaults={
                    'student_id': basic.id,
                    'birth_no': data.get('birth_no',''),
                    'birth_attach': data.get('birth_attach',''),
                    'nid_no': data.get('nid_no',''),
                    'nid_attach': data.get('nid_attach',''),
                    'marksheet': data.get('marksheet',''),
                }
            )
        except Exception:
            pass

        return Response({
            'success': True,
            'student_id': basic.id,
            'reg_no': reg_no,
            'students_type': students_type_val,
            'board_id_saved': board_id,
            'irregular_year_saved': irregular_year
        }, status=201)
