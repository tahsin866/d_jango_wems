from rest_framework import serializers
from apps.school.models import School
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
    madrasa_name = serializers.CharField(source='madrasa.mname', read_only=True)
    elhaqno = serializers.CharField(source='madrasa.elhaqno', read_only=True)

    class Meta:
        model = AssociatedMadrasa
        fields = [
            'id', 'fazilat', 'sanabiya_ulya', 'sanabiya', 'mutawassita', 'ibtedaiyyah',
            'hifzul_quran', 'qirat', 'noc_file_path', 'resolution_file_path',
            'markaz_application', 'madrasa', 'madrasa_name', 'elhaqno'
        ]

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'

class MarkazApplicationEditSerializer(serializers.ModelSerializer):
    associated_madrasas = AssociatedMadrasaSerializer(many=True)

    class Meta:
        model = MarkazApplication
        fields = ['markaz_type', 'requirements', 'exam', 'user', 'status', 'main_madrasa_info', 'associated_madrasas', 'deleted_madrasa_ids', 'attachments']