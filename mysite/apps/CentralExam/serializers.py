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

    # __init__ override removed; queryset set directly above

    class Meta:
        model = ExamFee
        fields = '__all__'
        extra_kwargs = {
            'exam_setup': {'required': False, 'allow_null': True},
            'marhala': {'required': False, 'allow_null': True},
            'reg_date_from': {'required': False, 'allow_null': True},
            'reg_date_to': {'required': False, 'allow_null': True},
            'reg_regular_fee': {'required': False, 'allow_null': True},
            'reg_irregular_jemni': {'required': False, 'allow_null': True},
            'reg_irregular_manonnoyon': {'required': False, 'allow_null': True},
            'reg_irregular_others': {'required': False, 'allow_null': True},
            'late_date_from': {'required': False, 'allow_null': True},
            'late_date_to': {'required': False, 'allow_null': True},
            'late_regular_fee': {'required': False, 'allow_null': True},
            'late_irregular_jemni': {'required': False, 'allow_null': True},
            'late_irregular_manonnoyon': {'required': False, 'allow_null': True},
            'late_irregular_others': {'required': False, 'allow_null': True},
        }
        extra_kwargs = {
            'exam_setup': {'required': True},
            'exam_name': {'required': True},
            'reg_date_from': {'required': False, 'allow_null': True},
            'reg_date_to': {'required': False, 'allow_null': True},
            'reg_regular_fee': {'required': False, 'allow_null': True},
            'reg_irregular_jemni': {'required': False, 'allow_null': True},
            'reg_irregular_manonnoyon': {'required': False, 'allow_null': True},
            'reg_irregular_others': {'required': False, 'allow_null': True},
            'late_date_from': {'required': False, 'allow_null': True},
            'late_date_to': {'required': False, 'allow_null': True},
            'late_regular_fee': {'required': False, 'allow_null': True},
            'late_irregular_jemni': {'required': False, 'allow_null': True},
            'late_irregular_manonnoyon': {'required': False, 'allow_null': True},
            'late_irregular_others': {'required': False, 'allow_null': True},
        }