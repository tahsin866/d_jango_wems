from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

import jwt
import json
from datetime import datetime, timedelta
import bcrypt
import secrets

from .serializers import (
    UserLoginHistorySerializer,
    UserFailedAttemptsSerializer,
    UserActivityLogSerializer,
    UserSessionsSerializer,
    UserTokensSerializer
)
from .auth_cache import cache_user_auth, get_cached_user_auth
from .models import User, UserLoginHistory, UserSessions, UserTokens, UserFailedAttempts

def get_user_id_from_request(request):
    user_id = request.session.get('user_id')
    if not user_id:
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token[7:]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('user_id')
            except Exception:
                user_id = None
    return user_id

# Helper functions to create user activity records
def _create_login_history(user, request, status):
    ip_address = request.META.get('REMOTE_ADDR', '')
    device = request.META.get('HTTP_USER_AGENT', '')
    browser = request.META.get('HTTP_USER_AGENT', '')
    UserLoginHistory.objects.create(
        user=user,
        ip_address=ip_address,
        device=device,
        browser=browser,
        status=status
    )

def _create_user_session(user, request):
    ip_address = request.META.get('REMOTE_ADDR', '')
    device = request.META.get('HTTP_USER_AGENT', '')
    browser = request.META.get('HTTP_USER_AGENT', '')
    session_token = secrets.token_hex(32)
    expires_at = datetime.utcnow() + timedelta(hours=24)
    UserSessions.objects.create(
        user=user,
        session_token=session_token,
        ip_address=ip_address,
        device=device,
        browser=browser,
        expires_at=expires_at
    )
    return session_token

def _create_user_token(user, token):
    expires_at = datetime.utcnow() + timedelta(hours=24)
    UserTokens.objects.create(
        user=user,
        token=token,
        expires_at=expires_at
    )

def _create_failed_attempt(user, request):
    ip_address = request.META.get('REMOTE_ADDR', '')
    UserFailedAttempts.objects.create(
        user=user,
        ip_address=ip_address,
        reason='Invalid credentials'
    )

class SecureAuthMixin:
    """Mixin for secure authentication methods"""
    
    def get_user_permissions(self, user_id, user_type):
        """Get user permissions based on user type"""
        with connection.cursor() as cursor:
            if user_type in ['Master Admin', 'Super Admin', 'Board Admin', 'Admin']:
                # Admin users get all permissions
                cursor.execute("""
                    SELECT DISTINCT m.id, m.name, mn.id as menu_id, mn.name as menu_name, mn.href
                    FROM modules m
                    LEFT JOIN menus mn ON m.id = mn.module_id
                    ORDER BY m.id, mn.id
                """)
            else:
                # Regular users get role-based permissions
                cursor.execute("""
                    SELECT DISTINCT m.id, m.name, mn.id as menu_id, mn.name as menu_name, mn.href
                    FROM modules m
                    LEFT JOIN menus mn ON m.id = mn.module_id
                    LEFT JOIN role_permissions rp ON m.id = rp.module_id
                    LEFT JOIN user_roles ur ON rp.role_id = ur.role_id
                    WHERE ur.user_id = %s
                    ORDER BY m.id, mn.id
                """, [user_id])
            
            return cursor.fetchall()

    def generate_secure_token(self, user_data):
        """Generate JWT token with user permissions"""
        payload = {
            'user_id': user_data['user_id'],
            'email': user_data['email'],
            'user_type': user_data['user_type'],
            'admin_category': user_data.get('admin_category'),
            'permissions': user_data.get('permissions', []),
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=24)  # 24 hour expiry
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    def validate_token(self, token):
        """Validate JWT token and return user data"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

@method_decorator(csrf_exempt, name='dispatch')
class SecureSigninView(View, SecureAuthMixin):
    """Secure signin with role-based access control"""
    
    def options(self, request, *args, **kwargs):
        response = JsonResponse({'detail': 'CORS preflight'})
        response["Access-Control-Allow-Origin"] = "http://localhost:5173"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Allow-Credentials"] = "true"
        return response

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('email') or data.get('phone') or data.get('phone_or_email')
            password = data.get('password')
            
            if not username or not password:
                return self.error_response('Email/Phone and password are required', 400)
            
            user_data = self.authenticate_user(username, password)
            
            if not user_data:
                try:
                    user = User.objects.get(email=username)
                    _create_failed_attempt(user, request)
                except User.DoesNotExist:
                    pass # User not found, do nothing
                return self.error_response('Invalid credentials', 401)
            
            user = User.objects.get(id=user_data['user_id'])

            if user_data['status'] != 'active':
                _create_login_history(user, request, 'failed')
                return self.error_response('Account is not active', 403)
            
            _create_login_history(user, request, 'success')
            session_token = _create_user_session(user, request)
            
            permissions = self.get_user_permissions(user_data['user_id'], user_data['user_type'])
            user_data['permissions'] = permissions
            
            token = self.generate_secure_token(user_data)
            _create_user_token(user, token)

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            
            dashboard_url = self.get_dashboard_url(user_data['user_type'])
            
            response_data = {
                'success': True,
                'access_token': token,
                'session_token': session_token,
                'user_type': user_data['user_type'],
                'user_id': user_data['user_id'],
                'redirect': dashboard_url,
                'permissions': len(permissions)
            }
            
            cache_key = f"user_auth:{username}"
            cache_user_auth(cache_key, response_data, expire=3600)
            
            response = JsonResponse(response_data)
            response["Access-Control-Allow-Origin"] = "http://localhost:5173"
            response["Access-Control-Allow-Credentials"] = "true"
            return response
            
        except Exception as e:
            return self.error_response(f'Authentication error: {str(e)}', 500)
    
    def authenticate_user(self, username, password):
        """Authenticate user against database"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT u.id, u.email, u.phone, u.password, ut.name as user_type, 
                       u.status, u.name, ac.name as admin_category
                FROM users u
                LEFT JOIN user_types ut ON u.user_type_id = ut.id
                LEFT JOIN admin_categories ac ON u.admin_category_id = ac.id
                WHERE LOWER(u.email) = LOWER(%s) OR u.phone = %s
            """, [username, username])
            
            row = cursor.fetchone()
            if not row:
                return None
            
            user_id, email, phone, db_password, user_type, status, name, admin_category = row
            
            password_valid = False
            if db_password.startswith('pbkdf2_'):
                from django.contrib.auth.hashers import check_password
                password_valid = check_password(password, db_password)
            else:
                try:
                    password_valid = bcrypt.checkpw(password.encode('utf-8'), db_password.encode('utf-8'))
                except:
                    password_valid = False
            
            if password_valid:
                return {
                    'user_id': user_id,
                    'email': email,
                    'phone': phone,
                    'user_type': user_type,
                    'status': status,
                    'name': name,
                    'admin_category': admin_category
                }
            return None
    
    def get_dashboard_url(self, user_type):
        """Get appropriate dashboard URL based on user type"""
        admin_types = ['Master Admin', 'Super Admin', 'Board Admin', 'Admin']
        
        if user_type in admin_types:
            return '/AdminDashboard'
        elif user_type == 'madrasha' or user_type == 'Madrasah':
            return '/dashboard'
        else:
            return '/dashboard'
    
    def error_response(self, message, status_code):
        response = JsonResponse({'success': False, 'error': message}, status=status_code)
        response["Access-Control-Allow-Origin"] = "http://localhost:5173"
        response["Access-Control-Allow-Credentials"] = "true"
        return response

@method_decorator(csrf_exempt, name='dispatch')
class SecureLogoutView(View):
    """Secure logout that clears all sessions"""
    
    def post(self, request):
        logout(request)
        response = JsonResponse({'success': True, 'message': 'Logged out successfully'})
        response["Access-Control-Allow-Origin"] = "http://localhost:5173"
        response["Access-Control-Allow-Credentials"] = "true"
        return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """Get authenticated user profile with security checks"""
    try:
        user_id = request.session.get('user_id')
        
        if not user_id:
            return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT u.id, u.name, u.email, u.phone, ut.name as user_type, 
                       ui.photo, ui.admin_designation, ac.name as admin_category
                FROM users u
                LEFT JOIN user_types ut ON u.user_type_id = ut.id
                LEFT JOIN user_information ui ON u.id = ui.user_id
                LEFT JOIN admin_categories ac ON u.admin_category_id = ac.id
                WHERE u.id = %s AND u.status = 'active'
            """, [user_id])
            
            row = cursor.fetchone()
            if not row:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
            user_id, name, email, phone, user_type, photo, admin_designation, admin_category = row
            
            photo_url = None
            if photo:
                photo_url = f"{request.scheme}://{request.get_host()}/media/{photo}"
            
            return Response({
                'success': True,
                'user': {
                    'id': user_id,
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'user_type': user_type,
                    'admin_designation': admin_designation,
                    'admin_category': admin_category,
                    'photo_url': photo_url
                }
            })
            
    except Exception as e:
        return Response({'error': 'Server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def validate_route_access(request):
    """Enhanced route validation with layout-based access control"""
    try:
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token[7:]
        else:
            token = request.data.get('token')
        
        route = request.data.get('route')
        
        if not token or not route:
            return Response({'valid': False, 'error': 'Token and route required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        mixin = SecureAuthMixin()
        payload = mixin.validate_token(token)
        
        if not payload:
            return Response({'valid': False, 'error': 'Invalid or expired token'}, 
                          status=status.HTTP_401_UNAUTHORIZED)
        
        user_type = payload.get('user_type')
        
        admin_layout_routes = ['/AdminDashboard', '/user/setup', '/marhala/setup', '/subject/setup']
        user_layout_routes = ['/dashboard', '/markaz/', '/student/', '/registr', '/payment', '/subject/list']
        
        admin_types = ['Master Admin', 'Super Admin', 'Board Admin', 'Admin']
        is_admin = user_type in admin_types
        
        if any(route.startswith(admin_route) for admin_route in admin_layout_routes):
            if not is_admin:
                return Response({
                    'valid': False, 
                    'error': 'Admin layout access denied',
                    'redirect_to': '/dashboard',
                    'user_type': user_type
                }, status=status.HTTP_403_FORBIDDEN)
        
        elif any(route.startswith(user_route) for user_route in user_layout_routes):
            if is_admin:
                return Response({
                    'valid': False, 
                    'error': 'User layout access denied for admin users',
                    'redirect_to': '/AdminDashboard',
                    'user_type': user_type
                }, status=status.HTTP_403_FORBIDDEN)
        
        return Response({
            'valid': True, 
            'user_type': user_type,
            'is_admin': is_admin,
            'route': route
        })
        
    except Exception as e:
        return Response({'valid': False, 'error': f'Validation error: {str(e)}'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)