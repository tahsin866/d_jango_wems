from rest_framework import serializers
from .models import RegistrationOverview, ExamSetup

class ExamSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSetup
        fields = ['id', 'exam_name']

class RegistrationOverviewSerializer(serializers.ModelSerializer):
    marhala_name_bn = serializers.CharField(source='marhala.marhala_name_bn', read_only=True)
    exam_setup = ExamSetupSerializer(read_only=True)
    exam_setup_id = serializers.PrimaryKeyRelatedField(
        queryset=ExamSetup.objects.all(), source='exam_setup', write_only=True
    )
    from apps.admin.subject.models import Marhala
    marhala_id = serializers.PrimaryKeyRelatedField(
        read_only=True, source='marhala'
    )

    class Meta:
        model = RegistrationOverview
        fields = [
            'id', 'marhala_name_bn', 'marhala_id', 'exam_setup', 'exam_setup_id',
            'reg_date_from', 'reg_date_to', 'reg_regular_fee',
            'reg_irregular_jemni', 'reg_irregular_manonnoyon', 'reg_irregular_others',
            'late_date_from', 'late_date_to', 'late_regular_fee',
            'late_irregular_jemni', 'late_irregular_manonnoyon', 'late_irregular_others',
            'created_at', 'updated_at'
        ]