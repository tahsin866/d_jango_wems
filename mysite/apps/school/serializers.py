from rest_framework import serializers
from .models import School

class SchoolCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['elhaqno', 'mobile', 'mname', 'village', 'post']
