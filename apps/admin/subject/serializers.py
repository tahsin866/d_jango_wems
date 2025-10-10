from rest_framework import serializers
from .models import Marhala, MarhalaSubject, SubjectSettings

class MarhalaSubjectSerializer(serializers.ModelSerializer):
    """মারহালা সাবজেক্ট সিরিয়ালাইজার"""
    class Meta:
        model = MarhalaSubject
        fields = '__all__'

class MarhalaWithCountsSerializer(serializers.ModelSerializer):
    """মারহালা উইথ কাউন্টস সিরিয়ালাইজার"""
    total_subjects = serializers.IntegerField(read_only=True)
    male_subjects = serializers.IntegerField(read_only=True)
    female_subjects = serializers.IntegerField(read_only=True)
    both_subjects = serializers.IntegerField(read_only=True)
    class Meta:
        model = Marhala
        fields = [
            'id', 
            'marhala_name_bn', 
            'marhala_name_en',
            'marhala_name_ar',
            'total_subjects',
            'male_subjects', 
            'female_subjects', 
            'both_subjects'
        ]

class MarhalaSerializer(serializers.ModelSerializer):
    """মারহালা সিরিয়ালাইজার"""
    class Meta:
        model = Marhala
        fields = '__all__'

class SubjectSettingsSerializer(serializers.ModelSerializer):
    """সাবজেক্ট সেটিংস সিরিয়ালাইজার"""
    marhala_name = serializers.CharField(source='marhala.marhala_name_bn', read_only=True)
    related_subject_code = serializers.CharField(source='subject.subject_code', read_only=True)
    marhala_id = serializers.IntegerField(source='marhala.id', read_only=True)
    subject_id = serializers.IntegerField(source='subject.id', read_only=True)
    class Meta:
        model = SubjectSettings
        fields = [
            'id',
            'marhala',
            'subject',
            'marhala_id',
            'subject_id',
            'marhala_name',
            'related_subject_code',
            'marhala_type',
            'subject_names',
            'student_type',
            'syllabus_type',
            'markaz_type',
            'subject_type',
            'total_marks',
            'pass_marks',
            'status',
            'subject_code',
            'created_at',
            'updated_at'
        ]