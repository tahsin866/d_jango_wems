from rest_framework import serializers
from .models import Division, District, Thana


class DivisionSerializer(serializers.ModelSerializer):
    """Division Serializer"""
    class Meta:
        model = Division
        fields = ['id', 'dname', 'division', 'username']


class DistrictSerializer(serializers.ModelSerializer):
    """District Serializer with division name"""
    division_name = serializers.CharField(source='division_ref.dname', read_only=True)

    class Meta:
        model = District
        fields = ['id', 'dname', 'district', 'username', 'desid', 'division_name']


class ThanaSerializer(serializers.ModelSerializer):
    """Thana Serializer with district name"""
    district_name = serializers.CharField(source='district_ref.dname', read_only=True)

    class Meta:
        model = Thana
        fields = ['id', 'dname', 'thana', 'username', 'des_id', 'thana_id', 'district_name']


class AddressDataSerializer(serializers.Serializer):
    """Combined Address Data Serializer"""
    division_name = serializers.CharField(read_only=True)
    district_name = serializers.CharField(read_only=True)
    thana_name = serializers.CharField(read_only=True)