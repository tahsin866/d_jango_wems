from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import OldStudentSerializer
from .models import student_basic, student_results

class OldStudentSearchView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        year = request.GET.get('year')
        roll_no = request.GET.get('roll_no')
        reg_no = request.GET.get('reg_no')
        marhala_id = request.GET.get('marhala')  # frontend param
        if not (year and roll_no and reg_no and marhala_id):
            return Response({'error': 'year, roll_no, reg_no, and marhala are required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            student = student_basic.objects.filter(year=year, roll_no=roll_no, reg_no=reg_no).first()
            if not student:
                return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)
            result = student_results.objects.filter(student_id=student.id, cid=marhala_id).first()
            data = {
                'student_name_bn': student.student_name_bn,
                'father_name_bn': student.father_name_bn,
                'mother_name_bn': '',
                'date_of_birth': student.date_of_birth,
                'class_name': result.class_name if result else '',
                'division': result.division if result else '',
                'roll_no': student.roll_no,
                'reg_no': student.reg_no,
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
