from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from apps.registration.OldStudent.models import student_basic
from apps.registration.StudentList.serializers import StudentBasicSerializer


class TestStudentAPIView(APIView):
    """
    Test API to fetch student data by ID from header
    Usage: Send student ID in header as 'X-Student-ID'
    """
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            # Get student ID from header
            student_id = request.headers.get('X-Student-ID')
            
            if not student_id:
                return Response({
                    'success': False,
                    'error': 'Student ID required in header (X-Student-ID)'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Try to convert to integer
            try:
                student_id = int(student_id)
            except ValueError:
                return Response({
                    'success': False,
                    'error': 'Invalid Student ID format'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Fetch student from student_basic table
            try:
                student = student_basic.objects.get(id=student_id)
            except student_basic.DoesNotExist:
                return Response({
                    'success': False,
                    'error': f'Student with ID {student_id} not found'
                }, status=status.HTTP_404_NOT_FOUND)

            # Serialize student data
            serializer = StudentBasicSerializer(student)
            
            return Response({
                'success': True,
                'message': f'Student data fetched successfully for ID: {student_id}',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'success': False,
                'error': f'Internal server error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)