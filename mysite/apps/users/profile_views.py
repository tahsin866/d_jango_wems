from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from mysite.apps.users.auth_views import SecureAuthMixin
import json


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_profile(request):
    """Get user profile information including name, email, user_type and photo"""
    try:
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token[7:]
        else:
            return Response({'error': 'Token required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Validate token
        mixin = SecureAuthMixin()
        payload = mixin.validate_token(token)
        
        if not payload:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = payload.get('user_id')
        if not user_id:
            return Response({'error': 'User ID not found in token'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get user profile data with joins including school/madrasha info
        with connection.cursor() as cursor:
            # Debug query to check what data is available
            cursor.execute("""
                SELECT 
                    u.id as user_id,
                    u.name as user_name,
                    u.email,
                    u.user_type_id,
                    ut.name as user_type_name,
                    ui.photo,
                    ui.madrasha_id,
                    s.id as school_id,
                    s.mname as madrasha_name
                FROM users u
                LEFT JOIN user_types ut ON u.user_type_id = ut.id
                LEFT JOIN user_information ui ON u.id = ui.user_id
                LEFT JOIN schools s ON ui.madrasha_id = s.id
                WHERE u.id = %s
            """, [user_id])
            
            row = cursor.fetchone()
            if not row:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Build user profile data
            user_profile = {
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'user_type_id': row[3],
                'user_type_name': row[4],
                'photo': row[5],
                'madrasha_id': row[6],
                'school_id': row[7],
                'madrasha_name': row[8] if row[8] else 'মাদ্রাসার তথ্য নেই',
                'is_admin': row[4] in ['Master Admin', 'Super Admin', 'Board Admin', 'Admin'] if row[4] else False,
                'avatar_url': None
            }
            
            # Generate photo URL if photo exists
            if user_profile['photo']:
                # Assuming photos are stored in media/user_photos/ directory
                user_profile['avatar_url'] = f"/media/user_photos/{user_profile['photo']}"
            
            return Response({
                'success': True,
                'user': user_profile
            }, status=status.HTTP_200_OK)
            
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Profile fetch error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def update_user_profile(request):
    """Update user profile information"""
    try:
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token[7:]
        else:
            return Response({'error': 'Token required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Validate token
        mixin = SecureAuthMixin()
        payload = mixin.validate_token(token)
        
        if not payload:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = payload.get('user_id')
        data = request.data
        
        with connection.cursor() as cursor:
            # Update users table
            if 'name' in data or 'email' in data:
                update_fields = []
                update_values = []
                
                if 'name' in data:
                    update_fields.append('name = %s')
                    update_values.append(data['name'])
                
                if 'email' in data:
                    update_fields.append('email = %s')
                    update_values.append(data['email'])
                
                update_values.append(user_id)
                
                cursor.execute(f"""
                    UPDATE users 
                    SET {', '.join(update_fields)}
                    WHERE id = %s
                """, update_values)
        
        return Response({
            'success': True,
            'message': 'Profile updated successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Profile update error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def upload_profile_photo(request):
    """Upload user profile photo"""
    try:
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token[7:]
        else:
            return Response({'error': 'Token required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Validate token
        mixin = SecureAuthMixin()
        payload = mixin.validate_token(token)
        
        if not payload:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = payload.get('user_id')
        
        if 'photo' not in request.FILES:
            return Response({'error': 'No photo file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        photo = request.FILES['photo']
        
        # Validate file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
        if photo.content_type not in allowed_types:
            return Response({'error': 'Invalid file type. Only JPEG, PNG, GIF allowed'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Validate file size (max 5MB)
        if photo.size > 5 * 1024 * 1024:
            return Response({'error': 'File too large. Maximum size is 5MB'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Generate unique filename
        import os
        import uuid
        from django.conf import settings
        
        extension = os.path.splitext(photo.name)[1]
        filename = f"user_{user_id}_{uuid.uuid4().hex[:8]}{extension}"
        
        # Save file
        upload_path = os.path.join(settings.MEDIA_ROOT, 'user_photos')
        os.makedirs(upload_path, exist_ok=True)
        
        file_path = os.path.join(upload_path, filename)
        with open(file_path, 'wb+') as destination:
            for chunk in photo.chunks():
                destination.write(chunk)
        
        # Update database
        with connection.cursor() as cursor:
            # Check if user_information record exists
            cursor.execute("SELECT id FROM user_information WHERE user_id = %s", [user_id])
            if cursor.fetchone():
                cursor.execute("""
                    UPDATE user_information 
                    SET photo = %s 
                    WHERE user_id = %s
                """, [filename, user_id])
            else:
                cursor.execute("""
                    INSERT INTO user_information (user_id, photo)
                    VALUES (%s, %s)
                """, [user_id, filename])
        
        return Response({
            'success': True,
            'message': 'Photo uploaded successfully',
            'photo_url': f"/media/user_photos/{filename}"
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Photo upload error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_profile_fallback(request):
    """Fallback profile API without token for specific user"""
    try:
        # Get user_id from query parameter or default to 15
        user_id = request.GET.get('user_id', 15)
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    u.id as user_id,
                    u.name as user_name,
                    u.email,
                    u.user_type_id,
                    ut.name as user_type_name,
                    ui.photo,
                    ui.madrasha_id,
                    s.id as school_id,
                    s.mname as madrasha_name
                FROM users u
                LEFT JOIN user_types ut ON u.user_type_id = ut.id
                LEFT JOIN user_information ui ON u.id = ui.user_id
                LEFT JOIN schools s ON ui.madrasha_id = s.id
                WHERE u.id = %s
            """, [user_id])
            
            row = cursor.fetchone()
            if not row:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Build user profile data
            user_profile = {
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'user_type_id': row[3],
                'user_type_name': row[4],
                'photo': row[5],
                'madrasha_id': row[6],
                'madrasha_name': row[8] if row[8] else 'মাদ্রাসার তথ্য নেই',
                'is_admin': row[4] in ['Master Admin', 'Super Admin', 'Board Admin', 'Admin'] if row[4] else False,
                'avatar_url': None
            }
            
            # Generate photo URL if photo exists
            if user_profile['photo']:
                user_profile['avatar_url'] = f"/media/user_photos/{user_profile['photo']}"
            
            return Response({
                'success': True,
                'user': user_profile
            }, status=status.HTTP_200_OK)
            
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Fallback profile error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def debug_user_data(request, user_id):
    """Debug API to check user data for specific user_id"""
    try:
        with connection.cursor() as cursor:
            # Check users table
            cursor.execute("SELECT id, name, email, user_type_id FROM users WHERE id = %s", [user_id])
            user_data = cursor.fetchone()
            
            # Check user_information table
            cursor.execute("SELECT user_id, madrasha_id, phone, address, photo FROM user_information WHERE user_id = %s", [user_id])
            user_info_data = cursor.fetchone()
            
            # Check schools table if madrasha_id exists
            school_data = None
            if user_info_data and user_info_data[1]:  # madrasha_id
                cursor.execute("SELECT id, mname FROM schools WHERE id = %s", [user_info_data[1]])
                school_data = cursor.fetchone()
            
            # Full join query
            cursor.execute("""
                SELECT 
                    u.id as user_id,
                    u.name as user_name,
                    u.email,
                    u.user_type_id,
                    ut.name as user_type_name,
                    ui.user_id as ui_user_id,
                    ui.madrasha_id,
                    ui.phone,
                    ui.address,
                    ui.photo,
                    s.id as school_id,
                    s.mname as madrasha_name
                FROM users u
                LEFT JOIN user_types ut ON u.user_type_id = ut.id
                LEFT JOIN user_information ui ON u.id = ui.user_id
                LEFT JOIN schools s ON ui.madrasha_id = s.id
                WHERE u.id = %s
            """, [user_id])
            
            joined_data = cursor.fetchone()
            
            return Response({
                'success': True,
                'user_id': user_id,
                'users_table': user_data,
                'user_information_table': user_info_data,
                'schools_table': school_data,
                'joined_query_result': joined_data,
                'debug_info': {
                    'has_user': bool(user_data),
                    'has_user_info': bool(user_info_data),
                    'has_madrasha_id': bool(user_info_data and user_info_data[1]),
                    'has_school_data': bool(school_data),
                }
            }, status=status.HTTP_200_OK)
            
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Debug error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
