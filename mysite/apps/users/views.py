from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.db import connection
from .models import Module, User, UserType, AdminCategory
from .serializers import ModuleSerializer, UserRegistrationSerializer
from .signup_views import UserSignupView

class ModuleListAPIView(generics.ListAPIView):
    queryset = Module.objects.prefetch_related('menus').all()
    serializer_class = ModuleSerializer

@api_view(['GET'])
def get_user_modules_menus(request):
    """Get modules and menus based on user permissions"""
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')
    
    # Debug session data
    # print(f"Session data: user_id={user_id}, user_type={user_type}")
    # print(f"All session keys: {list(request.session.keys())}")
    
    if not user_id or not user_type:
        return Response({
            'error': 'User not authenticated', 
            'debug': {
                'user_id': user_id,
                'user_type': user_type,
                'session_keys': list(request.session.keys())
            }
        }, status=401)
    
    # Master Admin gets all modules and menus
    if user_type == 'Master Admin':
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT m.id, m.name, m.description,
                       COALESCE(
                           json_agg(
                               json_build_object(
                                   'id', mn.id,
                                   'name', mn.name,
                                   'description', mn.description,
                                   'href', mn.href,
                                   'icon', mn.icon
                               ) ORDER BY mn.id
                           ) FILTER (WHERE mn.id IS NOT NULL), 
                           '[]'
                       ) as menus
                FROM modules m
                LEFT JOIN menus mn ON m.id = mn.module_id
                GROUP BY m.id, m.name, m.description
                ORDER BY m.id
            """)
            
            modules = []
            for row in cursor.fetchall():
                module_id, name, description, menus = row
                modules.append({
                    'id': module_id,
                    'name': name,
                    'description': description,
                    'menus': menus
                })
            
            return Response({'modules': modules})
    
    # For other users, check permissions
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT m.id, m.name, m.description,
                   COALESCE(
                       json_agg(
                           json_build_object(
                               'id', mn.id,
                               'name', mn.name,
                               'description', mn.description,
                               'href', mn.href,
                               'icon', mn.icon
                           ) ORDER BY mn.id
                       ) FILTER (WHERE mn.id IS NOT NULL), 
                       '[]'
                   ) as menus
            FROM modules m
            LEFT JOIN menus mn ON m.id = mn.module_id
            LEFT JOIN role_permissions rp ON m.id = rp.module_id
            LEFT JOIN user_roles ur ON rp.role_id = ur.role_id
            WHERE ur.user_id = %s
            GROUP BY m.id, m.name, m.description
            ORDER BY m.id
        """, [user_id])
        
        modules = []
        for row in cursor.fetchall():
            module_id, name, description, menus = row
            modules.append({
                'id': module_id,
                'name': name,
                'description': description,
                'menus': menus
            })
        
        return Response({'modules': modules})

@api_view(['GET'])
@permission_classes([AllowAny])
def debug_session(request):
    """Debug session data"""
    return Response({
        'session_data': dict(request.session),
        'user_authenticated': request.user.is_authenticated,
        'user_id': getattr(request.user, 'id', None),
        'user_email': getattr(request.user, 'email', None)
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def test_modules(request):
    """Test endpoint to get all modules without authentication"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT m.id, m.name, m.description,
                   COALESCE(
                       json_agg(
                           json_build_object(
                               'id', mn.id,
                               'name', mn.name,
                               'description', mn.description,
                               'href', mn.href,
                               'icon', mn.icon
                           ) ORDER BY mn.id
                       ) FILTER (WHERE mn.id IS NOT NULL), 
                       '[]'
                   ) as menus
            FROM modules m
            LEFT JOIN menus mn ON m.id = mn.module_id
            GROUP BY m.id, m.name, m.description
            ORDER BY m.id
        """)
        
        modules = []
        for row in cursor.fetchall():
            module_id, name, description, menus = row
            modules.append({
                'id': module_id,
                'name': name,
                'description': description,
                'menus': menus
            })
        
        return Response({'modules': modules})