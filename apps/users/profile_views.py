from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from apps.users.auth_views import SecureAuthMixin
import json
from datetime import datetime


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_profile(request):
    print("[DEBUG] get_user_profile called")
    try:
        token = request.headers.get('Authorization')
        print("[DEBUG] Authorization header:", token)
        if token and token.startswith('Bearer '):
            token = token[7:]
        else:
            return Response({'error': 'Token required'}, status=status.HTTP_401_UNAUTHORIZED)

        # Validate session_token
        with connection.cursor() as cursor:
            cursor.execute("SELECT user_id, expires_at, is_active FROM user_sessions WHERE session_token = %s", [token])
            session_row = cursor.fetchone()
            print("[DEBUG] Session row result:", session_row)

            if not session_row:
                return Response({'error': 'Invalid or expired session token'}, status=status.HTTP_401_UNAUTHORIZED)

            user_id, expires_at, is_active = session_row
            print("[DEBUG] Using user_id:", user_id)

            if not is_active:
                return Response({'error': 'Session inactive'}, status=status.HTTP_401_UNAUTHORIZED)
            if expires_at and expires_at < datetime.now():
                return Response({'error': 'Session expired'}, status=status.HTTP_401_UNAUTHORIZED)

        # Fetch user profile
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
                LEFT JOIN schools s ON ui.madrasha_id = s.school_id
                WHERE u.id = %s
            """, [user_id])

            row = cursor.fetchone()
            print("[DEBUG] User profile row:", row)

            if not row:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

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

            if user_profile['photo']:
                user_profile['avatar_url'] = f"/media/user_photos/{user_profile['photo']}"

            return Response({'success': True, 'user': user_profile}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'success': False, 'error': f'Profile fetch error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def update_user_profile(request):
    print("[DEBUG] update_user_profile called")
    try:
        token = request.headers.get('Authorization')
        print("[DEBUG] Authorization header:", token)
        if token and token.startswith('Bearer '):
            token = token[7:]
        else:
            return Response({'error': 'Token required'}, status=status.HTTP_401_UNAUTHORIZED)

        # Validate session_token
        with connection.cursor() as cursor:
            cursor.execute("SELECT user_id FROM user_sessions WHERE session_token = %s AND is_active = true", [token])
            session_row = cursor.fetchone()
            print("[DEBUG] Session row result:", session_row)

            if not session_row:
                return Response({'error': 'Invalid or expired session'}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = session_row[0]
            print("[DEBUG] Using user_id:", user_id)

        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        madrasha_id = data.get('madrasha_id')

        with connection.cursor() as cursor:
            cursor.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", [name, email, user_id])
            cursor.execute("UPDATE user_information SET madrasha_id=%s WHERE user_id=%s", [madrasha_id, user_id])

        return Response({'success': True, 'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'success': False, 'error': f'Update error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def upload_profile_photo(request):
    print("[DEBUG] upload_profile_photo called")
    try:
        token = request.headers.get('Authorization')
        print("[DEBUG] Authorization header:", token)
        if token and token.startswith('Bearer '):
            token = token[7:]
        else:
            return Response({'error': 'Token required'}, status=status.HTTP_401_UNAUTHORIZED)

        # Validate session_token
        with connection.cursor() as cursor:
            cursor.execute("SELECT user_id FROM user_sessions WHERE session_token = %s AND is_active = true", [token])
            session_row = cursor.fetchone()
            print("[DEBUG] Session row result:", session_row)

            if not session_row:
                return Response({'error': 'Invalid or expired session'}, status=status.HTTP_401_UNAUTHORIZED)

            user_id = session_row[0]
            print("[DEBUG] Using user_id:", user_id)

        photo = request.FILES.get('photo')
        if not photo:
            return Response({'error': 'No photo uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        file_path = f"user_photos/{user_id}_{photo.name}"
        with open(f"media/{file_path}", 'wb+') as destination:
            for chunk in photo.chunks():
                destination.write(chunk)

        with connection.cursor() as cursor:
            cursor.execute("UPDATE user_information SET photo=%s WHERE user_id=%s", [file_path, user_id])

        return Response({'success': True, 'photo_url': f"/media/{file_path}"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'success': False, 'error': f'Photo upload error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_profile_fallback(request):
    print("[DEBUG] get_profile_fallback called")
    user_id = request.GET.get('user_id')
    if user_id is None:
        return Response({'error': 'user_id query parameter required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user_id_int = int(user_id)
    except Exception:
        return Response({'error': 'Invalid user_id'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name, email FROM users WHERE id=%s", [user_id_int])
            row = cursor.fetchone()
            print("[DEBUG] User row:", row)

            if not row:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            return Response({'success': True, 'user': {'id': row[0], 'name': row[1], 'email': row[2]}}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def debug_user_data(request):
    print("[DEBUG] debug_user_data called")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users LIMIT 5")
            rows = cursor.fetchall()
            print("[DEBUG] Sample rows:", rows)

        return Response({'success': True, 'sample_users': rows}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
