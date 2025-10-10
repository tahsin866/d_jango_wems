from rest_framework import serializers
from .models import StudentBasic


class StudentBasicSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentBasic model
    Maps database fields to frontend requirements
    """
    # Frontend mapping fields
    student_image = serializers.CharField(source='photo', read_only=True)
    name_bn = serializers.CharField(source='student_name_bn', read_only=True)
    Date_of_birth = serializers.DateField(source='date_of_birth', read_only=True)
    student_type = serializers.CharField(source='students_type', read_only=True)
    current_class = serializers.CharField(source='marhala_name', read_only=True)
    current_madrasha = serializers.CharField(source='madrasha_name', read_only=True)
    exam_name_Bn = serializers.CharField(source='exam_name', read_only=True)
    
    # Computed fields for frontend compatibility
    payment_status = serializers.CharField(read_only=True)
    is_paid = serializers.BooleanField(read_only=True)

    class Meta:
        model = StudentBasic
        fields = [
            # Primary identification
            'id',
            'reg_no',
            
            # Frontend mapped fields
            'student_image',
            'name_bn', 
            'father_name_bn',
            'current_madrasha',
            'exam_name_Bn',
            'current_class',
            'Date_of_birth',
            'student_type',
            'payment_status',
            'is_paid',
            'status',
            
            # Original database fields (for reference)
            'photo',
            'student_name_bn',
            'student_name_ar',
            'student_name_en',
            'father_name_ar',
            'father_name_en',
            'mother_name_bn',
            'mother_name_ar',
            'mother_name_en',
            'roll_no',
            'year',
            'mobile',
            'marhala_id',
            'cid',
            'srtype',
            'hijri_year',
            'bangla_year',
            'students_type',
            'exam_id',
            'madrasha_id',
            'markaz_id',
            'is_old',
            'irregular_sub',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class StudentBasicListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing students
    Only includes essential fields for table display
    """
    student_image = serializers.CharField(source='photo', read_only=True)
    name_bn = serializers.CharField(source='student_name_bn', read_only=True)
    Date_of_birth = serializers.DateField(source='date_of_birth', read_only=True)
    student_type = serializers.CharField(source='students_type', read_only=True)
    current_class = serializers.CharField(source='marhala_name', read_only=True)
    current_madrasha = serializers.CharField(source='madrasha_name', read_only=True)
    exam_name_Bn = serializers.CharField(source='exam_name', read_only=True)
    payment_status = serializers.CharField(read_only=True)
    is_paid = serializers.BooleanField(read_only=True)

    class Meta:
        model = StudentBasic
        fields = [
            'id',
            'reg_no',
            'student_image',
            'name_bn',
            'father_name_bn',
            'current_madrasha',
            'exam_name_Bn',
            'current_class',
            'Date_of_birth',
            'student_type',
            'payment_status',
            'is_paid',
            'status'
        ]


class StudentBasicCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating students
    """
    class Meta:
        model = StudentBasic
        fields = [
            'photo',
            'student_name_bn',
            'student_name_ar',
            'student_name_en',
            'father_name_bn',
            'father_name_ar',
            'father_name_en',
            'mother_name_bn',
            'mother_name_ar',
            'mother_name_en',
            'roll_no',
            'reg_no',
            'year',
            'date_of_birth',
            'mobile',
            'status',
            'marhala_id',
            'cid',
            'srtype',
            'hijri_year',
            'bangla_year',
            'students_type',
            'exam_id',
            'madrasha_id',
            'markaz_id',
            'is_old',
            'irregular_sub'
        ]

    def validate_reg_no(self, value):
        """Validate registration number uniqueness"""
        if value:
            existing = StudentBasic.objects.filter(reg_no=value)
            if self.instance:
                existing = existing.exclude(id=self.instance.id)
            if existing.exists():
                raise serializers.ValidationError("এই রেজিস্ট্রেশন নম্বর ইতিমধ্যে ব্যবহৃত হয়েছে।")
        return value

    def validate_mobile(self, value):
        """Validate mobile number format"""
        if value and len(value) > 0:
            # Basic mobile number validation for Bangladesh
            if not value.startswith(('01', '+8801')) or len(value) not in [11, 14]:
                raise serializers.ValidationError("মোবাইল নম্বর সঠিক ফরম্যাটে দিন।")
        return value