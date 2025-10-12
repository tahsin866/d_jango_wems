from rest_framework import serializers

class NewStudentSerializer(serializers.Serializer):
    # Personal
    student_name_bn = serializers.CharField(required=True)
    student_name_ar = serializers.CharField(required=False, allow_blank=True)
    student_name_en = serializers.CharField(required=False, allow_blank=True)
    father_name_bn = serializers.CharField(required=False, allow_blank=True)
    father_name_ar = serializers.CharField(required=False, allow_blank=True)
    father_name_en = serializers.CharField(required=False, allow_blank=True)
    mother_name_bn = serializers.CharField(required=False, allow_blank=True)
    mother_name_ar = serializers.CharField(required=False, allow_blank=True)
    mother_name_en = serializers.CharField(required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    mobile = serializers.CharField(required=False, allow_blank=True)

    # IDs / relations
    marhala_id = serializers.IntegerField(required=False, allow_null=True)
    madrasha_id = serializers.IntegerField(required=False, allow_null=True)
    markaz_id = serializers.IntegerField(required=False, allow_null=True)

    # Board related (new)
    board_id = serializers.IntegerField(required=False, allow_null=True)
    irregular_year = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    # Address (IDs expected like OldStudent logic expects)
    division_id = serializers.CharField(required=False, allow_blank=True)
    district_id = serializers.CharField(required=False, allow_blank=True)
    thana_id = serializers.CharField(required=False, allow_blank=True)

    # Attachments
    birth_no = serializers.CharField(required=False, allow_blank=True)
    birth_attach = serializers.CharField(required=False, allow_blank=True)
    nid_no = serializers.CharField(required=False, allow_blank=True)
    nid_attach = serializers.CharField(required=False, allow_blank=True)
    marksheet = serializers.CharField(required=False, allow_blank=True)
    passport_photo = serializers.CharField(required=False, allow_blank=True)
    student_image = serializers.CharField(required=False, allow_blank=True)

    # Misc
    students_type = serializers.CharField(required=False, allow_blank=True)
    exam_id = serializers.IntegerField(required=False, allow_null=True)
    cid = serializers.IntegerField(required=False, allow_null=True)
    srtype = serializers.IntegerField(required=False, allow_null=True)
    irregular_sub = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        # Force students_type logic based on board selection
        board_id = attrs.get('board_id')
        # If board chosen and not the main Befaq board (id logic left to view), set irregular/regular logic in view
        return attrs
