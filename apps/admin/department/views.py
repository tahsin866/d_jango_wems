from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from .models import Department
from .serializers import (
    DepartmentSerializer,
    UserTypeSerializer,
    ModuleSerializer,
    MenuSerializer,
    PermissionSerializer
)
from apps.users.models import Module, Menu, Permission, UserType

User = get_user_model()


class DepartmentListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class ModuleListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer


class MenuListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class PermissionListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class UserTypeListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def get_modules_by_department(request, department_id):
    """Get modules filtered by department_id"""
    modules = Module.objects.filter(department_id=department_id)
    serializer = ModuleSerializer(modules, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_menus_by_module(request, module_id):
    """Get menus filtered by module_id"""
    menus = Menu.objects.filter(module_id=module_id)
    serializer = MenuSerializer(menus, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_department_name(request, department_id):
    """Get department name by department_id"""
    try:
        department = Department.objects.get(id=department_id)
        return Response({
            'success': True,
            'department_id': department.id,
            'department_name': department.name
        })
    except Department.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Department not found'
        }, status=404)


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def get_user_permissions(request, user_id):
#     """Get permissions for a specific user"""
#     # UserMenuPermission model commented out as table doesn't exist
#     # user_permissions = UserMenuPermission.objects.filter(user_id=user_id)
#     # serializer = UserMenuPermissionSerializer(user_permissions, many=True)
#     return Response({'message': 'User permissions feature disabled'}, status=404)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def save_user_permissions(request, user_id):
#     """Save permissions for a specific user"""
#     # UserMenuPermission model commented out as table doesn't exist
#     return Response({'message': 'User permissions feature disabled'}, status=404)