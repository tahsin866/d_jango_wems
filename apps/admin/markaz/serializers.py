from rest_framework import serializers
from apps.Markaz.models import MadrashaCenter
from apps.school.models import School
from apps.admin.madrasha.models import Division, District, Thana

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

CENTER_TYPE_MAP = {
    1: "দারসিয়াত",
    2: "হিফজ",
    3: "কিরাআত"
}

class MadrashaCenterListSerializer(serializers.ModelSerializer):
    """Serializer for MadrashaCenter data with School information joined"""
    stage_display = serializers.SerializerMethodField()
    student_type_display = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    division_name = serializers.SerializerMethodField()
    district_name = serializers.SerializerMethodField()
    thana_name = serializers.SerializerMethodField()

    # MadrashaCenter fields
    center_id = serializers.IntegerField(read_only=True)
    serial_number = serializers.CharField(read_only=True)
    center_name_display = serializers.SerializerMethodField()

    # School fields that will be joined
    mname = serializers.SerializerMethodField()
    ara_mname = serializers.SerializerMethodField()
    elhaqno = serializers.SerializerMethodField()
    mtype = serializers.SerializerMethodField()
    stage = serializers.SerializerMethodField()
    stageserial = serializers.SerializerMethodField()
    village = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()
    enabledisable = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    mmlabel = serializers.SerializerMethodField()
    editdate = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    school_id = serializers.SerializerMethodField()

    class Meta:
        model = MadrashaCenter
        fields = [
            # MadrashaCenter fields
            'id', 'madrasha_id', 'center_id', 'serial_number', 'center_name_display',
            # Joined School fields
            'mname', 'ara_mname', 'elhaqno', 'mtype', 'stage', 'stageserial',
            'village', 'post', 'mobile', 'enabledisable', 'status', 'year',
            'mmlabel', 'editdate', 'created_at', 'updated_at', 'school_id',
            # Display fields
            'division_name', 'district_name', 'thana_name',
            'stage_display', 'student_type_display', 'location'
        ]

    def get_school_data(self, obj):
        """Helper method to get school data"""
        if not obj.madrasha_id:
            return None

        try:
            # Find school by school_id field (since both madrasha_id and school_id contain the same values)
            school = School.objects.filter(school_id=obj.madrasha_id).first()
            if not school:
                # Try finding by id field as fallback
                school = School.objects.filter(id=obj.madrasha_id).first()
            return school
        except Exception as e:
            # Log the error for debugging
            print(f"Error getting school data for madrasha_id {obj.madrasha_id}: {e}")
            return None

    def get_center_name_display(self, obj):
        """Get the display name for the center type"""
        if obj.center_id:
            return CENTER_TYPE_MAP.get(obj.center_id, f"কেন্দ্র {obj.center_id}")
        return None

    def get_mname(self, obj):
        school = self.get_school_data(obj)
        return school.mname if school else None

    def get_ara_mname(self, obj):
        school = self.get_school_data(obj)
        return school.ara_mname if school else None

    def get_elhaqno(self, obj):
        school = self.get_school_data(obj)
        return school.elhaqno if school else None

    def get_mtype(self, obj):
        school = self.get_school_data(obj)
        return school.mtype if school else None

    def get_stage(self, obj):
        school = self.get_school_data(obj)
        return school.stage if school else None

    def get_stageserial(self, obj):
        school = self.get_school_data(obj)
        return school.stageserial if school else None

    def get_village(self, obj):
        school = self.get_school_data(obj)
        return school.village if school else None

    def get_post(self, obj):
        school = self.get_school_data(obj)
        return school.post if school else None

    def get_mobile(self, obj):
        school = self.get_school_data(obj)
        return school.mobile if school else None

    def get_enabledisable(self, obj):
        school = self.get_school_data(obj)
        if school and school.status:
            return '1' if school.status == '1' else '0'
        return '0'

    def get_status(self, obj):
        school = self.get_school_data(obj)
        return school.status if school else None

    def get_year(self, obj):
        school = self.get_school_data(obj)
        return school.year if school else None

    def get_mmlabel(self, obj):
        school = self.get_school_data(obj)
        return school.mmlabel if school else None

    def get_editdate(self, obj):
        school = self.get_school_data(obj)
        return school.editdate if school else None

    def get_created_at(self, obj):
        school = self.get_school_data(obj)
        return school.created_at if school else None

    def get_updated_at(self, obj):
        school = self.get_school_data(obj)
        return school.updated_at if school else None

    def get_school_id(self, obj):
        school = self.get_school_data(obj)
        return school.school_id if school else None

    def get_stage_display(self, obj):
        school = self.get_school_data(obj)
        if school and hasattr(school, 'stage') and school.stage is not None:
            return STAGE_MAP.get(str(school.stage), str(school.stage))
        return None

    def get_student_type_display(self, obj):
        school = self.get_school_data(obj)
        if school and hasattr(school, 'mtype') and school.mtype is not None:
            return STUDENT_TYPE_MAP.get(str(school.mtype), str(school.mtype))
        return None

    def get_location(self, obj):
        school = self.get_school_data(obj)
        if school:
            division = self.get_division_name(school)
            district = self.get_district_name(school)
            thana = self.get_thana_name(school)
            if division or district or thana:
                return f"{division or ''}, {district or ''}, {thana or ''}".replace(', , ', ', ').strip(', ')
        return None

    def get_division_name(self, school):
        if not school or not hasattr(school, 'did') or school.did is None:
            return None
        # Ensure we're working with a School object, not MadrashaCenter
        if school.__class__.__name__ != 'School':
            return None
        try:
            division = Division.objects.get(id=school.did)
            return division.division
        except Division.DoesNotExist:
            return None

    def get_district_name(self, school):
        if not school or not hasattr(school, 'des_id') or school.des_id is None:
            return None
        # Ensure we're working with a School object, not MadrashaCenter
        if school.__class__.__name__ != 'School':
            return None
        try:
            district = District.objects.get(desid=school.des_id)
            return district.district
        except District.DoesNotExist:
            return None

    def get_thana_name(self, school):
        if not school or not hasattr(school, 'tid') or school.tid is None:
            return None
        # Ensure we're working with a School object, not MadrashaCenter
        if school.__class__.__name__ != 'School':
            return None
        try:
            thana = Thana.objects.get(thana_id=school.tid)
            return thana.thana
        except Thana.DoesNotExist:
            return None