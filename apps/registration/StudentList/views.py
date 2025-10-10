from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404

from .service import (
    get_student_list,
    get_student_detail,
    create_student,
    update_student,
    delete_student,
    get_student_statistics,
    bulk_update_students
)


@method_decorator(csrf_exempt, name='dispatch')
class StudentListView(APIView):
    """
    API View for listing students with pagination and filtering
    GET /api/registration/students/
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            # Get query parameters
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
            
            # Build filters from query parameters
            filters = {}
            if request.GET.get('search'):
                filters['search'] = request.GET.get('search')
            if request.GET.get('marhala_id'):
                filters['marhala_id'] = int(request.GET.get('marhala_id'))
            if request.GET.get('exam_id'):
                filters['exam_id'] = int(request.GET.get('exam_id'))
            if request.GET.get('madrasha_id'):
                filters['madrasha_id'] = int(request.GET.get('madrasha_id'))
            if request.GET.get('students_type'):
                filters['students_type'] = request.GET.get('students_type')
            if request.GET.get('status'):
                filters['status'] = request.GET.get('status')
            if request.GET.get('year'):
                filters['year'] = int(request.GET.get('year'))
            
            # Get user ID from request
            user_id = getattr(request.user, 'id', None) if hasattr(request, 'user') else None
            
            # Get student list
            result = get_student_list(
                user_id=user_id,
                filters=filters,
                page=page,
                page_size=page_size
            )
            
            return Response({
                'success': True,
                'data': result['students'],
                'pagination': result['pagination'],
                'filters': result['filters_applied']
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({
                'success': False,
                'error': f'Invalid parameter: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Internal server error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class StudentDetailView(APIView):
    """
    API View for individual student operations
    GET /api/registration/students/{id}/
    PUT /api/registration/students/{id}/
    DELETE /api/registration/students/{id}/
    """
    permission_classes = [AllowAny]
    
    def get(self, request, pk):
        try:
            # Get user ID from request
            user_id = getattr(request.user, 'id', None) if hasattr(request, 'user') else None
            
            student_data = get_student_detail(pk, user_id=user_id)
            if student_data:
                return Response({
                    'success': True,
                    'data': student_data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'error': 'Student not found'
                }, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Internal server error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, pk):
        try:
            user_id = getattr(request.user, 'id', None) if hasattr(request, 'user') else None
            student, error = update_student(pk, request.data, user_id)
            
            if student:
                return Response({
                    'success': True,
                    'message': 'Student updated successfully',
                    'data': {'id': student.id}
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'error': error
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Internal server error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        try:
            user_id = getattr(request.user, 'id', None) if hasattr(request, 'user') else None
            success, message = delete_student(pk, user_id)
            
            if success:
                return Response({
                    'success': True,
                    'message': message
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'error': message
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Internal server error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class StudentCreateView(APIView):
    """
    API View for creating new students
    POST /api/registration/students/create/
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            user_id = getattr(request.user, 'id', None) if hasattr(request, 'user') else None
            student, error = create_student(request.data, user_id)
            
            if student:
                return Response({
                    'success': True,
                    'message': 'Student created successfully',
                    'data': {'id': student.id, 'reg_no': student.reg_no}
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'success': False,
                    'error': error
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Internal server error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class StudentStatisticsView(APIView):
    """
    API View for student statistics
    GET /api/registration/students/statistics/
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            # Get user ID from request
            user_id = getattr(request.user, 'id', None) if hasattr(request, 'user') else None
            
            stats = get_student_statistics(user_id=user_id)
            return Response({
                'success': True,
                'data': stats
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Internal server error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class StudentBulkUpdateView(APIView):
    """
    API View for bulk updating students
    POST /api/registration/students/bulk-update/
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            student_updates = request.data.get('students', [])
            if not student_updates:
                return Response({
                    'success': False,
                    'error': 'No student data provided'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user_id = getattr(request.user, 'id', None) if hasattr(request, 'user') else None
            result = bulk_update_students(student_updates, user_id)
            
            return Response({
                'success': True,
                'message': f'Bulk update completed: {result["success_count"]} successful, {result["error_count"]} failed',
                'data': result
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Internal server error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name='dispatch')
class StudentSearchView(APIView):
    """
    API View for advanced student search
    GET /api/registration/students/search/
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            # Get search parameters
            search_term = request.GET.get('q', '').strip()
            if not search_term:
                return Response({
                    'success': False,
                    'error': 'Search term is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Build filters
            filters = {'search': search_term}
            
            # Optional filters
            if request.GET.get('marhala_id'):
                filters['marhala_id'] = int(request.GET.get('marhala_id'))
            if request.GET.get('exam_id'):
                filters['exam_id'] = int(request.GET.get('exam_id'))
            
            # Get page parameters
            page = int(request.GET.get('page', 1))
            page_size = min(int(request.GET.get('page_size', 20)), 50)  # Max 50 results
            
            user_id = getattr(request.user, 'id', None) if hasattr(request, 'user') else None
            
            result = get_student_list(
                user_id=user_id,
                filters=filters,
                page=page,
                page_size=page_size
            )
            
            return Response({
                'success': True,
                'data': result['students'],
                'pagination': result['pagination'],
                'search_term': search_term
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({
                'success': False,
                'error': f'Invalid parameter: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'error': f'Internal server error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)