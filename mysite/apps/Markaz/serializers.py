from rest_framework import serializers
from mysite.apps.school.models import School
from .models import MarkazApplication, MainMadrasaInfo, AssociatedMadrasa, Attachment

class SchoolSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'mname', 'elhaqno']

class MarkazApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkazApplication
        fields = '__all__'

class MainMadrasaInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainMadrasaInfo
        fields = '__all__'

class AssociatedMadrasaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssociatedMadrasa
        fields = '__all__'

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'

class MarkazApplicationEditSerializer(serializers.ModelSerializer):
    associated_madrasas = AssociatedMadrasaSerializer(many=True)

    class Meta:
        model = MarkazApplication
        fields = ['markaz_type', 'requirements', 'exam', 'user', 'status', 'main_madrasa_info', 'associated_madrasas', 'deleted_madrasa_ids', 'attachments']