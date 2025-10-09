from rest_framework import serializers
from apps.school.models import School
from .models import MarkazApplication, MainMadrasaInfo, AssociatedMadrasa, Attachment

class SchoolSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'mname', 'elhaqno', 'school_id']  # school_id যোগ করা হয়েছে

class MarkazApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkazApplication
        fields = '__all__'

class MainMadrasaInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainMadrasaInfo
        fields = '__all__'

class AssociatedMadrasaSerializer(serializers.ModelSerializer):
    # madrasa_id দিয়ে school খুঁজে নাম এবং elhaqno পাওয়া
    madrasa_name = serializers.SerializerMethodField()
    elhaqno = serializers.SerializerMethodField()

    class Meta:
        model = AssociatedMadrasa
        fields = [
            'id', 'fazilat', 'sanabiya_ulya', 'sanabiya', 'mutawassita', 'ibtedaiyyah',
            'hifzul_quran', 'qirat', 'noc_file_path', 'resolution_file_path',
            'markaz_application', 'madrasa_id', 'madrasa_name', 'elhaqno'
        ]

    def validate_madrasa_id(self, value):
        """Validate that the madrasa_id exists in School table"""
        if value:
            from apps.school.models import School
            # Try to find school by either school_id or id
            school = School.objects.filter(school_id=str(value)).first()
            if not school:
                school = School.objects.filter(id=value).first()
            if not school:
                raise serializers.ValidationError(f"School with ID {value} not found")
        return value

    def get_madrasa_name(self, obj):
        if obj.madrasa_id:
            from apps.school.models import School
            # String হিসেবেও try করি
            school = School.objects.filter(school_id=str(obj.madrasa_id)).first()
            if not school:
                school = School.objects.filter(id=obj.madrasa_id).first()
            return school.mname if school else None
        return None

    def get_elhaqno(self, obj):
        if obj.madrasa_id:
            from apps.school.models import School
            # String হিসেবেও try করি
            school = School.objects.filter(school_id=str(obj.madrasa_id)).first()
            if not school:
                school = School.objects.filter(id=obj.madrasa_id).first()
            return school.elhaqno if school else None
        return None

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'

class MarkazApplicationEditSerializer(serializers.ModelSerializer):
    associated_madrasas = AssociatedMadrasaSerializer(many=True)

    class Meta:
        model = MarkazApplication
        fields = ['markaz_type', 'requirements', 'exam', 'user', 'status', 'main_madrasa_info', 'associated_madrasas', 'deleted_madrasa_ids', 'attachments']