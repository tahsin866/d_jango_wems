import jwt
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db import connection

User = get_user_model()

class SecureJWTAuthMiddleware:
    """Enhanced JWT middleware with layout-based role access control"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Define layout-based route access patterns
        self.admin_layout_routes = [
            '/AdminDashboard',
            '/admin/',
            '/user/setup',
            '/marhala/setup', 
            '/subject/setup'
        ]
        
        self.user_layout_routes = [
            '/dashboard',
            '/markaz/',
            '/student/',
            '/registr',
            '/payment',
            '/subject/list',
            '/confirmation',
            '/restore',
            '/old'
        ]
        
        self.public_routes = [
            '/',
            '/signin',
            '/signup',
            '/auth/',
            '/static/',
            '/media/',
            '/error-404',
            '/unauthorized',
            '/api/auth/',
            '/validate-signup-token'
        ]
        
        # Admin user types
        self.admin_types = ['Master Admin', 'Super Admin', 'Board Admin', 'Admin']

    def __call__(self, request):
        # Skip middleware for public routes
        if self.is_public_route(request.path):
            return self.get_response(request)
        
        # Check for JWT token
        token = self.get_token_from_request(request)
        
        if token:
            payload = self.validate_token(token)
            if payload:
                user_type = payload.get('user_type')
                
                # Layout-based route validation
                layout_violation = self.check_layout_violation(request.path, user_type)
                if layout_violation:
                    return JsonResponse({
                        'error': 'Layout access denied',
                        'message': layout_violation['message'],
                        'redirect_to': layout_violation['redirect'],
                        'user_type': user_type,
                        'path': request.path
                    }, status=403)
                
                # Attach user info to request
                request.jwt_user = payload
                
                # Set user in Django auth system
                try:
                    user = User.objects.get(email=payload.get('email'))
                    request.user = user
                except User.DoesNotExist:
                    pass
            else:
                # Invalid token for protected route
                if not self.is_public_route(request.path):
                    return JsonResponse({'error': 'Invalid or expired token'}, status=401)
        else:
            # No token for protected route
            if not self.is_public_route(request.path):
                return JsonResponse({'error': 'Authentication required'}, status=401)

        response = self.get_response(request)
        return response
    
    def is_public_route(self, path):
        """Check if route is public"""
        return any(path.startswith(route) for route in self.public_routes)
    
    def get_token_from_request(self, request):
        """Extract JWT token from request"""
        # Try Authorization header first
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            return auth_header[7:]
        
        # Try from cookies
        return request.COOKIES.get('access_token')
    
    def validate_token(self, token):
        """Validate JWT token"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            
            # Additional validation - check if user still exists and is active
            user_id = payload.get('user_id')
            if user_id:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT status FROM users WHERE id = %s
                    """, [user_id])
                    row = cursor.fetchone()
                    if not row or row[0] != 'active':
                        return None
            
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def check_layout_violation(self, path, user_type):
        """Check if user is trying to access wrong layout"""
        is_admin = user_type in self.admin_types
        
        # Check if admin trying to access user layout
        if is_admin and any(path.startswith(route) for route in self.user_layout_routes):
            return {
                'message': f'Admin users cannot access user layout routes',
                'redirect': '/AdminDashboard'
            }
        
        # Check if non-admin trying to access admin layout
        if not is_admin and any(path.startswith(route) for route in self.admin_layout_routes):
            return {
                'message': f'Non-admin users cannot access admin layout routes',
                'redirect': '/dashboard'
            }
        
        return None  # No violation
    
    def validate_route_access(self, path, user_type):
        """Legacy method - kept for backward compatibility"""
        return self.check_layout_violation(path, user_type) is None
    
    def get_required_role(self, path):
        """Get required role for path"""
        if any(path.startswith(route) for route in self.admin_only_routes):
            return 'Admin'
        elif any(path.startswith(route) for route in self.madrasa_only_routes):
            return 'madrasha'
        return 'Any'

# Keep the old middleware for backward compatibility
class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get('Authorization')
        if token and token.startswith('Bearer '):
            token = token[7:]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user = User.objects.get(id=payload['user_id'])
                request.user = user
                request.user_type = payload.get('user_type', 'madrasha')
            except (jwt.InvalidTokenError, User.DoesNotExist):
                pass

        response = self.get_response(request)
        return response
