# apps/school/serializers.py

STAGE_MAP = {
    "1": "তাকমিল",
    "2": "ফযিলত",
    "3": "সানাবিয়া উলইয়া",
    "4": "সানাবিয়া",
    "5": "মুতাওয়াসসিতাহ",
    "6": "ইবতেদাইয়্যাহ",
    "7": "হিফজুল কোরাআন",
    "8": "কিরাআত"
}

STUDENT_TYPE_MAP = {
    "0": "ছাত্রী",
    "1": "ছাত্র"
}

from rest_framework import serializers
from .models import School

class SchoolCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['elhaqno', 'mobile', 'mname', 'village', 'post', 'school_id']

class SchoolListSerializer(serializers.ModelSerializer):
    stage_display = serializers.SerializerMethodField()
    student_type_display = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    division_name = serializers.SerializerMethodField()
    district_name = serializers.SerializerMethodField()
    thana_name = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = [
            'id', 'madrasha_id', 'mtype', 'elhaqno', 'stage', 'stageserial', 'mnname', 'ara_mname', 'mname',
            'did', 'des_id', 'tid', 'village', 'post', 'mobile', 'enabledisable', 'year', 'mmlabel',
            'editdate', 'created_at', 'updated_at', 'school_id', 'status',
            'division_name', 'district_name', 'thana_name',
            'stage_display', 'student_type_display', 'location'
        ]
        
    def get_stage_display(self, obj):
        return STAGE_MAP.get(str(obj.stage), obj.stage)

    def get_student_type_display(self, obj):
        return STUDENT_TYPE_MAP.get(str(obj.mtype), obj.mtype)

    def get_location(self, obj):
        division = self.get_division_name(obj)
        district = self.get_district_name(obj)
        thana = self.get_thana_name(obj)
        return f"{division}, {district}, {thana}"

    def get_division_name(self, obj):
        from apps.admin.madrasha.models import Division
        try:
            # Division টেবিলের id ফিল্ড দিয়ে খুঁজুন
            division = Division.objects.get(id=obj.did)
            return division.division  # dname ফিল্ড থেকে নাম নিন
        except Division.DoesNotExist:
            return None

    def get_district_name(self, obj):
        from apps.admin.madrasha.models import District
        try:
            # District টেবিলের desid ফিল্ড দিয়ে খুঁজুন
            district = District.objects.get(desid=obj.des_id)
            return district.district
        except District.DoesNotExist:
            return None

    def get_thana_name(self, obj):
        from apps.admin.madrasha.models import Thana
        try:
            # Thana টেবিলের thana_id ফিল্ড দিয়ে খুঁজুন
            thana = Thana.objects.get(thana_id=obj.tid)
            return thana.thana
        except Thana.DoesNotExist:
            return None