from rest_framework import serializers
from .models import Department
from apps.users.models import Module, Menu, Permission, UserType


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'head_user_id']

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ['id', 'name', 'description']

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'name', 'description', 'icon', 'department_id']

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'module_id', 'name', 'description', 'href', 'icon']

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'description']

# UserMenuPermissionSerializer commented out as table doesn't exist
# class UserMenuPermissionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserMenuPermission
#         fields = ['user', 'menu', 'permission', 'created_at']