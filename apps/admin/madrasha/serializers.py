# apps/admin/madrasha/serializers.py

from rest_framework import serializers
from .models import Division, District, Thana

class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = ['id', 'division']  # id এবং dname ফিল্ড রিটার্ন করুন

class DistrictSerializer(serializers.ModelSerializer):
    division_name = serializers.CharField(source='division.division', read_only=True)

    class Meta:
        model = District
        fields = ['id', 'did', 'desid', 'district', 'division_name']

class ThanaSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.division', read_only=True)

    class Meta:
        model = Thana
        fields = ['id', 'des_id', 'thana_id', 'thana', 'district_name']