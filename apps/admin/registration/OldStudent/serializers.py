from rest_framework import serializers

class OldStudentSerializer(serializers.Serializer):
    student_name_bn = serializers.CharField()
    father_name_bn = serializers.CharField()
    mother_name_bn = serializers.CharField(allow_blank=True)
    date_of_birth = serializers.DateField()
    class_name = serializers.CharField(allow_blank=True)
    division = serializers.CharField(allow_blank=True)
    roll_no = serializers.CharField()
    reg_no = serializers.CharField()
