from rest_framework import serializers
from .models import ExamSetup


class ExamSetupSerializer(serializers.ModelSerializer):
    """কেন্দ্রীয় পরীক্ষা সেটআপ সিরিয়ালাইজার"""
    
    class Meta:
        model = ExamSetup
        fields = [
            'id',
            'exam_name',
            'arabic_year',
            'bangla_year', 
            'english_year',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_exam_name(self, value):
        """পরীক্ষার নাম validation"""
        if not value or not value.strip():
            raise serializers.ValidationError("পরীক্ষার নাম অবশ্যই প্রয়োজন")
        return value.strip()
    
    def validate_arabic_year(self, value):
        """আরবি বছর validation"""
        if not value or not value.strip():
            raise serializers.ValidationError("আরবি বছর অবশ্যই প্রয়োজন")
        return value.strip()
    
    def validate_bangla_year(self, value):
        """বাংলা বছর validation"""
        if not value or not value.strip():
            raise serializers.ValidationError("বাংলা বছর অবশ্যই প্রয়োজন")
        return value.strip()
    
    def validate_english_year(self, value):
        """ইংরেজি বছর validation"""
        if not value or not value.strip():
            raise serializers.ValidationError("ইংরেজি বছর অবশ্যই প্রয়োজন")
        return value.strip()