# serializers.py - FIXED VERSION
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
    """পরীক্ষার ফি সিরিয়ালাইজার - ✅ FIXED"""
    
    # ✅ Nested serializers for better response
    exam_setup_name = serializers.CharField(source='exam_setup.exam_name', read_only=True)
    marhala_name = serializers.CharField(source='marhala.name', read_only=True)
    
    class Meta:
        model = ExamFee
        fields = [
            'id',
            'exam_setup',  # ✅ ForeignKey field
            'exam_setup_name',  # ✅ Read-only display field
            'marhala',  # ✅ ForeignKey field (can be null)
            'marhala_name',  # ✅ Read-only display field
            'reg_date_from',
            'reg_date_to',
            'reg_regular_fee',
            'reg_irregular_jemni',
            'reg_irregular_manonnoyon',
            'reg_irregular_others',
            'late_date_from',
            'late_date_to',
            'late_regular_fee',
            'late_irregular_jemni',
            'late_irregular_manonnoyon',
            'late_irregular_others',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'exam_setup_name', 'marhala_name']
        extra_kwargs = {
            'exam_setup': {'required': True, 'allow_null': False},
            'marhala': {'required': False, 'allow_null': True},
        }

    def validate_exam_setup(self, value):
        """exam_setup validation"""
        if not value:
            raise serializers.ValidationError("পরীক্ষা সেটআপ অবশ্যই নির্বাচন করতে হবে")
        return value

    def validate_reg_date_range(self, attrs):
        """নিয়মিত ফি এর তারিখের রেঞ্জ চেক"""
        reg_from = attrs.get('reg_date_from')
        reg_to = attrs.get('reg_date_to')
        
        if reg_from and reg_to:
            if reg_from > reg_to:
                raise serializers.ValidationError({
                    'reg_date_to': 'নিয়মিত ফি এর শেষ তারিখ শুরুর তারিখের চেয়ে পরে হতে হবে'
                })
        return attrs

    def validate_late_date_range(self, attrs):
        """বিলম্ব ফি এর তারিখের রেঞ্জ চেক"""
        late_from = attrs.get('late_date_from')
        late_to = attrs.get('late_date_to')
        
        if late_from and late_to:
            if late_from > late_to:
                raise serializers.ValidationError({
                    'late_date_to': 'বিলম্ব ফি এর শেষ তারিখ শুরুর তারিখের চেয়ে পরে হতে হবে'
                })
        return attrs

    def validate(self, attrs):
        """সামগ্রিক validation"""
        attrs = self.validate_reg_date_range(attrs)
        attrs = self.validate_late_date_range(attrs)
        
        # ✅ Check for duplicate exam_setup + marhala combination (if updating)
        exam_setup = attrs.get('exam_setup')
        marhala = attrs.get('marhala')
        
        if exam_setup and marhala:
            # যদি এটি update operation হয়
            instance_id = self.instance.id if self.instance else None
            
            existing = ExamFee.objects.filter(
                exam_setup=exam_setup, 
                marhala=marhala
            )
            
            if instance_id:
                existing = existing.exclude(id=instance_id)
            
            if existing.exists():
                raise serializers.ValidationError({
                    'marhala': f'এই মারহালার জন্য ইতিমধ্যে ফি নির্ধারণ করা হয়েছে'
                })
        
        return attrs


class ExamFeeDetailSerializer(ExamFeeSerializer):
    """বিস্তারিত তথ্যের জন্য আলাদা সিরিয়ালাইজার"""
    
    # ✅ Full exam_setup object
    exam_setup_detail = ExamSetupSerializer(source='exam_setup', read_only=True)
    
    class Meta(ExamFeeSerializer.Meta):
        fields = ExamFeeSerializer.Meta.fields + ['exam_setup_detail']