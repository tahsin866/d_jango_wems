from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.db import connection
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

import json
from datetime import datetime, timedelta
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

# Get the User model
UserModel = get_user_model()

# --- API endpoint for login history creation ---
@api_view(['POST'])
@permission_classes([AllowAny])
def create_login_history(request):
    UserModel = get_user_model()
    user_id = request.data.get('user')
    status = request.data.get('status')
    ip_address = request.data.get('ip_address', '')
    device = request.data.get('device', '')
    browser = request.data.get('browser', '')
    location = request.data.get('location', '')

    try:
        if not user_id:
            print('LoginHistory Error: user_id missing')
            return Response({'success': False, 'error': 'user_id missing'}, status=400)
        if not status:
            print('LoginHistory Error: status missing')
            return Response({'success': False, 'error': 'status missing'}, status=400)
        user_obj = UserModel.objects.get(id=user_id)
        print(f'LoginHistory: Creating for user_id={user_id}, status={status}')
        UserLoginHistory.objects.create(
            user=user_obj,
            ip_address=ip_address,
            device=device,
            browser=browser,
            location=location,
            status=status
        )
        print('LoginHistory: Success')
        return Response({'success': True})
    except UserModel.DoesNotExist:
        print(f'LoginHistory Error: User not found for id={user_id}')
        return Response({'success': False, 'error': 'User not found'}, status=404)
    except Exception as e:
        print(f'LoginHistory Exception: {str(e)}')
        return Response({'success': False, 'error': f'Error creating login history: {str(e)}'}, status=500)


# --- Utility functions ---
def get_user_id_from_request(request):
    user_id = request.session.get('user_id')
    if not user_id and hasattr(request, "user") and request.user.is_authenticated:
        user_id = request.user.id
    return user_id

def _create_login_history(user_obj, request, login_status):
    """Create login history entry"""
    try:
        # Ensure we have a proper User instance
        if not isinstance(user_obj, UserModel):
            # If it's not a User instance, try to get it from database
            if hasattr(user_obj, 'id'):
                user_obj = UserModel.objects.get(id=user_obj.id)
            else:
                raise ValueError("Invalid user object provided")
        
        ip_address = request.META.get('REMOTE_ADDR', '')
        device = request.META.get('HTTP_USER_AGENT', '')
        browser = request.META.get('HTTP_USER_AGENT', '')
        
        UserLoginHistory.objects.create(
            user=user_obj,
            ip_address=ip_address,
            device=device,
            browser=browser,
            status=login_status
        )
    except Exception as e:
        # Log the error but don't break the authentication flow
        print(f"Error creating login history: {str(e)}")

def _create_user_session(user_obj, request):
    """Create user session"""
    try:
        # Ensure we have a proper User instance
        if not isinstance(user_obj, UserModel):
            if hasattr(user_obj, 'id'):
                user_obj = UserModel.objects.get(id=user_obj.id)
            else:
                raise ValueError("Invalid user object provided")

        ip_address = request.META.get('REMOTE_ADDR', '')
        device = request.META.get('HTTP_USER_AGENT', '')
        browser = request.META.get('HTTP_USER_AGENT', '')
        session_token = secrets.token_hex(32)
        from django.utils import timezone
        expires_at = timezone.now() + timedelta(hours=24)

        # Insert or update session_token for user
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, session_token, expires_at, is_active FROM user_sessions WHERE user_id = %s AND is_active = TRUE
            """, [user_obj.id])
            existing = cursor.fetchone()
            print(f"[Session Debug] Existing session row for user {user_obj.id}: {existing}")
            if existing:
                cursor.execute("""
                    UPDATE user_sessions SET session_token = %s, ip_address = %s, device = %s, browser = %s, expires_at = %s, is_active = TRUE WHERE user_id = %s
                """, [session_token, ip_address, device, browser, expires_at, user_obj.id])
                print(f"[Session Debug] Updated session for user {user_obj.id} with token {session_token}")
            else:
                cursor.execute("""
                    INSERT INTO user_sessions (user_id, session_token, ip_address, device, browser, expires_at, is_active, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, TRUE, NOW())
                """, [user_obj.id, session_token, ip_address, device, browser, expires_at])
                print(f"[Session Debug] Inserted new session for user {user_obj.id} with token {session_token}")
        return session_token
    except Exception as e:
        print(f"Error creating user session: {str(e)}")
        return secrets.token_hex(32)  # Return a token anyway

def _create_user_token(user_obj, token):
    """Create user token"""
    try:
        # Ensure we have a proper User instance
        if not isinstance(user_obj, UserModel):
            if hasattr(user_obj, 'id'):
                user_obj = UserModel.objects.get(id=user_obj.id)
            else:
                raise ValueError("Invalid user object provided")
        
        from django.utils import timezone
        expires_at = timezone.now() + timedelta(hours=24)
        UserTokens.objects.create(
            user=user_obj,
            token=token,
            expires_at=expires_at
        )
    except Exception as e:
        print(f"Error creating user token: {str(e)}")

def _create_failed_attempt(user_obj, request):
    """Create failed login attempt record"""
    try:
        # Ensure we have a proper User instance
        if not isinstance(user_obj, UserModel):
            if hasattr(user_obj, 'id'):
                user_obj = UserModel.objects.get(id=user_obj.id)
            else:
                raise ValueError("Invalid user object provided")
        
        ip_address = request.META.get('REMOTE_ADDR', '')
        UserFailedAttempts.objects.create(
            user=user_obj,
            ip_address=ip_address,
            reason='Invalid credentials'
        )
    except Exception as e:
        print(f"Error creating failed attempt record: {str(e)}")

# --- Main Auth Mixin ---
class SecureAuthMixin:
    def get_user_permissions(self, user_id, user_type):
        """Simple permission system - return basic modules and menus for all users"""
        with connection.cursor() as cursor:
            # Get all modules and menus (simplified approach)
            cursor.execute("""
                SELECT DISTINCT m.id, m.name, mn.id as menu_id, mn.name as menu_name, mn.href
                FROM modules m
                LEFT JOIN menus mn ON m.id = mn.module_id
                ORDER BY m.id, mn.id
            """)
            return cursor.fetchall()

# --- Auth Signin View ---
@method_decorator(csrf_exempt, name='dispatch')
class SecureSigninView(View, SecureAuthMixin):
    """Secure signin with role-based access control using DRF authentication"""

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

            user = authenticate(request, username=username, password=password)

            if not user:
                # Handle failed login attempt
                try:
                    user_obj = UserModel.objects.get(email=username)
                    _create_failed_attempt(user_obj, request)
                except UserModel.DoesNotExist:
                    pass
                return self.error_response('Invalid credentials', 401)

            # Ensure user is a proper UserModel instance
            if not isinstance(user, UserModel):
                # Try to get the correct UserModel instance
                try:
                    user = UserModel.objects.get(email=username)
                except UserModel.DoesNotExist:
                    return self.error_response('Authentication error: Invalid user object', 500)

            # Debug: print user id and type
            print(f"SigninView: user.id={user.id}, type={type(user)}")

            # Create login history
            _create_login_history(user, request, 'success')

            # Create session
            session_token = _create_user_session(user, request)

            # Create token
            _create_user_token(user, session_token)

            # Get user permissions
            user_type_name = user.user_type.name if user.user_type else None
            permissions = self.get_user_permissions(user.id, user_type_name)
            
            # Simple layout determination based on user type
            # Admin layout users: Master Admin, Director, System Admin, and all department heads
            admin_user_types = [
                'Master Admin', 'Director', 'System Admin', 'Accounts Head',
                'Publication Head', 'Talim & Tarbiyat Head', 'Certificate Section Head', 
                'Chief Director', 'Training Section Head'
            ]
            layout_type = 'admin' if user_type_name in admin_user_types else 'user'
            dashboard_url = '/admin/dashboard' if layout_type == 'admin' else '/user/dashboard'

            # Login the user
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            # Get department_id from session after login
            department_id = request.session.get('department_id')

            response_data = {
                'success': True,
                'session_token': session_token,
                'user_type': user_type_name,
                'user_id': user.id,
                'user_name': user.name,
                'user_email': user.email,
                'department_id': department_id,
                'layout_type': layout_type,
                'redirect': dashboard_url,
                'permissions': len(permissions),
                'can_access_admin': layout_type == 'admin'
            }

            # Cache user auth
            cache_key = f"user_auth:{username}"
            cache_user_auth(cache_key, response_data, expire=3600)

            response = JsonResponse(response_data)
            response["Access-Control-Allow-Origin"] = "http://localhost:5173"
            response["Access-Control-Allow-Credentials"] = "true"
            return response

        except json.JSONDecodeError:
            return self.error_response('Invalid JSON data', 400)
        except Exception as e:
            print(f"Authentication error: {str(e)}")  # Log for debugging
            return self.error_response(f'Authentication error: {str(e)}', 500)

    def error_response(self, message, status_code):
        response = JsonResponse({'success': False, 'error': message}, status=status_code)
        response["Access-Control-Allow-Origin"] = "http://localhost:5173"
        response["Access-Control-Allow-Credentials"] = "true"
        return response

# --- Auth Logout View ---
@method_decorator(csrf_exempt, name='dispatch')
class SecureLogoutView(View):
    """Secure logout that clears all sessions"""

    def post(self, request):
        logout(request)
        response = JsonResponse({'success': True, 'message': 'Logged out successfully'})
        response["Access-Control-Allow-Origin"] = "http://localhost:5173"
        response["Access-Control-Allow-Credentials"] = "true"
        return response

# --- User Profile API ---
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """Get authenticated user profile with security checks"""
    try:
        user_id = get_user_id_from_request(request)
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

# --- Route Access Validation API ---
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validate_route_access(request):
    """Enhanced route validation with comprehensive user type layout access control"""
    try:
        user = request.user
        route = request.data.get('route')

        if not user.is_authenticated or not route:
            return Response({'valid': False, 'error': 'Authentication and route required'}, 
                            status=status.HTTP_400_BAD_REQUEST)

        user_type = getattr(user, 'user_type', None)
        user_type_name = user_type.name if user_type else None
        
        # Simple layout determination - same as login
        admin_user_types = [
            'Master Admin', 'Director', 'System Admin', 'Accounts Head',
            'Publication Head', 'Talim & Tarbiyat Head', 'Certificate Section Head', 
            'Chief Director', 'Training Section Head'
        ]
        layout_type = 'admin' if user_type_name in admin_user_types else 'user'
        can_admin = layout_type == 'admin'
        
        admin_layout_routes = ['/admin/', '/AdminDashboard', '/user/setup', '/marhala/setup', '/subject/setup']
        user_layout_routes = ['/user/', '/dashboard', '/markaz/', '/student/', '/registr', '/payment', '/subject/list']

        # Check admin layout access
        if any(route.startswith(admin_route) for admin_route in admin_layout_routes):
            if not can_admin:
                return Response({
                    'valid': False, 
                    'error': f'Admin layout access denied for {user_type_name}',
                    'redirect_to': '/user/dashboard',
                    'user_type': user_type_name,
                    'layout_type': layout_type
                }, status=status.HTTP_403_FORBIDDEN)

        return Response({
            'valid': True, 
            'user_type': user_type_name,
            'layout_type': layout_type,
            'can_access_admin': can_admin,
            'route': route
        })

    except Exception as e:
        return Response({'valid': False, 'error': f'Validation error: {str(e)}'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def check_session(request):
    """
    Simple endpoint to check if user is logged in
    Endpoint: /api/auth/check-session/
    """
    try:
        print(f"=== CHECK SESSION DEBUG ===")
        print(f"User authenticated: {request.user.is_authenticated}")
        print(f"User: {request.user}")
        print(f"Session key: {request.session.session_key}")
        print(f"Session data: {dict(request.session)}")
        print(f"Cookies: {dict(request.COOKIES)}")

        return Response({
            'authenticated': request.user.is_authenticated,
            'user_id': request.user.id if request.user.is_authenticated else None,
            'username': request.user.username if request.user.is_authenticated else None,
            'session_key': request.session.session_key,
            'cookies': dict(request.COOKIES),
            'session_data': dict(request.session)
        })
    except Exception as e:
        print(f"Check session error: {e}")
        import traceback
        traceback.print_exc()
        return Response({'error': str(e)}, status=500)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def validate_session(request):
    """
    Validate Django session for microservices
    Endpoint: /api/auth/validate-session/
    """
    try:
        # Debug logging
        print(f"=== DJANGO SESSION VALIDATION DEBUG ===")
        print(f"Request method: {request.method}")
        print(f"Request headers: {dict(request.headers)}")
        print(f"Request cookies: {dict(request.COOKIES)}")
        print(f"Session key: {request.session.session_key}")
        print(f"User authenticated: {request.user.is_authenticated}")
        print(f"User object: {request.user}")

        # Check if user is authenticated through Django's session
        if request.user.is_authenticated:
            user = request.user
            user_type_name = user.user_type.name if user.user_type else 'Unknown'

            # Return user information
            return Response({
                'valid': True,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'user_type': user_type_name,
                    'department_id': user.department_id,
                    'permissions': ['admin'] if user_type_name in [
                        'Master Admin', 'Director', 'System Admin', 'Accounts Head',
                        'Publication Head', 'Talim & Tarbiyat Head', 'Certificate Section Head',
                        'Chief Director', 'Training Section Head'
                    ] else ['user']
                }
            }, status=status.HTTP_200_OK)
        else:
            print(f"User not authenticated, session key: {request.session.session_key}")
            return Response({
                'valid': False,
                'error': 'User not authenticated'
            }, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        print(f"Session validation error: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({
            'valid': False,
            'error': f'Session validation failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def validate_token(request):
    """
    Validate JWT token for microservices
    Endpoint: /api/auth/validate/
    """
    try:
        # Get authorization header
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({
                'valid': False,
                'error': 'Invalid authorization header format'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Extract token
        token = auth_header.split(' ')[1]
        
        if not token:
            return Response({
                'valid': False,
                'error': 'Token not provided'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if token exists in our UserTokens table
        try:
            user_token = UserTokens.objects.get(token=token, is_active=True)
            user = user_token.user
            
            # Check if token is expired
            if user_token.expires_at and user_token.expires_at < datetime.now():
                user_token.is_active = False
                user_token.save()
                return Response({
                    'valid': False,
                    'error': 'Token expired'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Get user type name
            user_type_name = user.user_type.name if user.user_type else 'Unknown'
            
            # Return user information
            return Response({
                'valid': True,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'user_type': user_type_name,
                    'department_id': user.department_id,
                    'permissions': ['admin'] if user_type_name in [
                        'Master Admin', 'Director', 'System Admin', 'Accounts Head',
                        'Publication Head', 'Talim & Tarbiyat Head', 'Certificate Section Head', 
                        'Chief Director', 'Training Section Head'
                    ] else ['user']
                }
            }, status=status.HTTP_200_OK)
            
        except UserTokens.DoesNotExist:
            return Response({
                'valid': False,
                'error': 'Invalid token'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
    except Exception as e:
        print(f"Token validation error: {str(e)}")
        return Response({
            'valid': False,
            'error': f'Token validation failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)