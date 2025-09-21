from rest_framework import serializers
from .models import ExamSetup, ExamFee

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
        if not value or not value.strip():
            raise serializers.ValidationError("পরীক্ষার নাম অবশ্যই প্রয়োজন")
        return value.strip()

    def validate_arabic_year(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("আরবি বছর অবশ্যই প্রয়োজন")
        return value.strip()

    def validate_bangla_year(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("বাংলা বছর অবশ্যই প্রয়োজন")
        return value.strip()



class ExamFeeSerializer(serializers.ModelSerializer):
    from mysite.apps.subject.models import Marhala
    marhala = serializers.PrimaryKeyRelatedField(queryset=Marhala.objects.all(), required=False, allow_null=True)
    
    class Meta:
        model = ExamFee
        fields = '__all__'
        extra_kwargs = {
            'exam_setup': {'required': True, 'allow_null': False},  # Required এবং null allow করা যাবে না
            'marhala': {'required': False, 'allow_null': True},
            'exam_name': {'required': False},  # এটা optional করা হলো
        }

    def validate_exam_setup(self, value):
        """exam_setup validation"""
        if not value:
            raise serializers.ValidationError("পরীক্ষা সেটআপ অবশ্যই নির্বাচন করতে হবে")
        return value