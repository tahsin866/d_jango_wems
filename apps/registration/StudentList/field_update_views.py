from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .service import update_student_field, update_student_address_field


@method_decorator(csrf_exempt, name='dispatch')
class StudentFieldUpdateView(APIView):
    """
    API View for updating individual student fields
    PATCH /api/registration/students/{id}/update/
    """
    permission_classes = [AllowAny]

    def patch(self, request, pk):
        try:
            user_id = request.data.get('user_id') or request.GET.get('user_id')

            # Get field name and value from request
            if not request.data:
                return Response({
                    'success': False,
                    'error': 'No update data provided'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Update each field provided
            updated_fields = []
            errors = []

            for field_name, field_value in request.data.items():
                if field_name == 'user_id':  # Skip user_id as it's not a field
                    continue

                success, message = update_student_field(pk, field_name, field_value, user_id)
                if success:
                    updated_fields.append(field_name)
                else:
                    errors.append(f"{field_name}: {message}")

            if updated_fields:
                return Response({
                    'success': True,
                    'message': f'Updated {len(updated_fields)} field(s): {", ".join(updated_fields)}',
                    'updated_fields': updated_fields,
                    'errors': errors if errors else None
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'error': 'No fields updated',
                    'errors': errors
                }, status=status.HTTP_400_BAD_REQUEST)

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


@method_decorator(csrf_exempt, name='dispatch')
class StudentAddressFieldUpdateView(APIView):
    """
    API View for updating individual student address fields
    PATCH /api/registration/students/{id}/update-address/
    """
    permission_classes = [AllowAny]

    def patch(self, request, pk):
        try:
            user_id = request.data.get('user_id') or request.GET.get('user_id')

            # Get field name and value from request
            if not request.data:
                return Response({
                    'success': False,
                    'error': 'No update data provided'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Update each field provided
            updated_fields = []
            errors = []

            for field_name, field_value in request.data.items():
                if field_name == 'user_id':  # Skip user_id as it's not a field
                    continue

                success, message = update_student_address_field(pk, field_name, field_value, user_id)
                if success:
                    updated_fields.append(field_name)
                else:
                    errors.append(f"{field_name}: {message}")

            if updated_fields:
                return Response({
                    'success': True,
                    'message': f'Updated {len(updated_fields)} address field(s): {", ".join(updated_fields)}',
                    'updated_fields': updated_fields,
                    'errors': errors if errors else None
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'error': 'No address fields updated',
                    'errors': errors
                }, status=status.HTTP_400_BAD_REQUEST)

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