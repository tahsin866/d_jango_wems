from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.db import transaction
from .models import Module, Menu, User, UserType, UserInformation, UserLoginHistory, UserFailedAttempts, UserActivityLog, UserSessions, UserTokens
class UserLoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLoginHistory
        fields = ['id', 'user', 'login_time', 'logout_time', 'ip_address', 'device', 'browser', 'location', 'status']

class UserFailedAttemptsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFailedAttempts
        fields = ['id', 'user', 'attempt_time', 'ip_address', 'reason']

class UserActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivityLog
        fields = ['id', 'user', 'action', 'request_path', 'meta_data', 'created_at']

class UserSessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSessions
        fields = ['id', 'user', 'session_token', 'created_at', 'expires_at', 'is_active', 'ip_address', 'device', 'browser']

class UserTokensSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTokens
        fields = ['id', 'user', 'token', 'issued_at', 'expires_at', 'revoked']
from apps.school.models import School

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name', 'description', 'href', 'icon']

class ModuleSerializer(serializers.ModelSerializer):
    menus = MenuSerializer(many=True, read_only=True)
    class Meta:
        model = Module
        fields = ['id', 'name', 'description', 'icon', 'menus']

class UserRegistrationSerializer(serializers.Serializer):
    # Form fields from frontend
    name = serializers.CharField(max_length=100)
    admin_Designation = serializers.CharField(max_length=100, source='admin_designation')
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    NID_no = serializers.CharField(max_length=20, source='nid_no')
    Mobile_no = serializers.CharField(max_length=20, required=False, allow_blank=True, source='whatsapp_no')
    phone = serializers.CharField(max_length=20)
    photo = serializers.ImageField(required=False)
    nid_photo = serializers.ImageField(required=False)
    
    # Additional fields from madrasha info
    madrasha_name = serializers.CharField(required=False, allow_blank=True)
    post = serializers.CharField(required=False, allow_blank=True)
    village = serializers.CharField(required=False, allow_blank=True)
    custom_code = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({'password_confirmation': 'পাসওয়ার্ড মিলছে না'})
        return data

    @transaction.atomic
    def create(self, validated_data):
        # Remove password confirmation as it's not needed for creation
        validated_data.pop('password_confirmation', None)
        
        # Get or create UserType for "madrasha"
        user_type, created = UserType.objects.get_or_create(
            name='madrasha',
            defaults={'description': 'account for madrasha users'}
        )
        
        # Find school_id from schools table based on madrasha info
        madrasha_school_id = None
        if validated_data.get('madrasha_name') and validated_data.get('village'):
            try:
                school = School.objects.filter(
                    mname__icontains=validated_data['madrasha_name'],
                    village__icontains=validated_data['village']
                ).first()
                if school:
                    madrasha_school_id = school.school_id  # Use school.school_id field as requested
                    print(f"Found school: {school.mname}, school_id: {school.school_id}, id: {school.id}")
            except Exception as e:
                print(f"Error finding school: {e}")
                pass
        
        # Prepare user data
        user_data = {
            'name': validated_data['name'],
            'phone': validated_data['phone'],
            'email': validated_data['email'],
            'password': make_password(validated_data['password']),
            'user_type': user_type,
        }
        
        # Create User
        user = User.objects.create(**user_data)
        
        # Prepare user information data
        user_info_data = {
            'user': user,
            'madrasha_id': madrasha_school_id,  # schools table এর school_id বসবে madrasha_id তে (যেমন 1439)
            'custom_code': validated_data.get('custom_code', ''),
            'admin_designation': validated_data.get('admin_designation', ''),
            'nid_no': validated_data.get('nid_no', ''),
            'whatsapp_no': validated_data.get('Mobile_no', ''),
            'photo': validated_data.get('photo'),
            'nid_photo': validated_data.get('nid_photo'),
        }
        
        # Create UserInformation
        user_info = UserInformation.objects.create(**user_info_data)
        
        return {
            'user': user,
            'user_info': user_info,
            'user_type_created': created
        }