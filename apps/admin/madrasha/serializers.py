from rest_framework import serializers
from .models import Division, District, Thana


class DivisionSerializer(serializers.ModelSerializer):
    did = serializers.IntegerField(source='id', read_only=True)  # Map id to did for API consistency

    class Meta:
        model = Division
        fields = ['did', 'division']

class DistrictSerializer(serializers.ModelSerializer):
    division_name = serializers.CharField(source='division.division', read_only=True)
    division_id = serializers.IntegerField(source='division.id', read_only=True)  # Changed from division.did to division.id

    class Meta:
        model = District
        fields = ['desid', 'district', 'division_name', 'division_id']

class ThanaSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.district', read_only=True)
    district_id = serializers.IntegerField(source='district.desid', read_only=True)

    class Meta:
        model = Thana
        fields = ['thana_id', 'thana', 'district_name', 'district_id']