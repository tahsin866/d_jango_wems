from django.db import models

class student_basic(models.Model):
    id = models.AutoField(primary_key=True)
    photo = models.CharField(max_length=255, blank=True, null=True)
    student_name_bn = models.CharField(max_length=255)
    student_name_ar = models.CharField(max_length=255, blank=True, null=True)
    student_name_en = models.CharField(max_length=255, blank=True, null=True)
    father_name_bn = models.CharField(max_length=255, blank=True, null=True)
    father_name_ar = models.CharField(max_length=255, blank=True, null=True)
    father_name_en = models.CharField(max_length=255, blank=True, null=True)
    mother_name_bn = models.CharField(max_length=255, blank=True, null=True)
    mother_name_ar = models.CharField(max_length=255, blank=True, null=True)
    mother_name_en = models.CharField(max_length=255, blank=True, null=True)
    roll_no = models.IntegerField()
    reg_no = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    marhala_id = models.IntegerField(blank=True, null=True)
    cid = models.IntegerField(blank=True, null=True)
    srtype = models.IntegerField(blank=True, null=True)
    hijri_year = models.IntegerField(blank=True, null=True)
    bangla_year = models.IntegerField(blank=True, null=True)
    students_type = models.CharField(max_length=255, blank=True, null=True)
    exam_id = models.IntegerField(blank=True, null=True)
    madrasha_id = models.IntegerField(blank=True, null=True)
    markaz_id = models.IntegerField(blank=True, null=True)
    is_old = models.IntegerField(blank=True, null=True)
    irregular_sub = models.IntegerField(blank=True, null=True)
    board_id = models.IntegerField(blank=True, null=True)
    irregular_year = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'student_basic'
        managed = False

class student_results(models.Model):
    id = models.BigAutoField(primary_key=True)
    student_id = models.BigIntegerField()
    madrasha = models.CharField(max_length=255, blank=True, null=True)
    mid = models.CharField(max_length=255, blank=True, null=True)
    class_name = models.CharField(max_length=255, blank=True, null=True)
    markaj = models.CharField(max_length=255, blank=True, null=True)
    marid = models.IntegerField(blank=True, null=True)
    melhaq = models.CharField(max_length=255, blank=True, null=True)
    subject_label = models.CharField(max_length=255, blank=True, null=True)
    subject_value = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    grace_label = models.CharField(max_length=255, blank=True, null=True)
    grace_value = models.IntegerField(blank=True, null=True)
    positions = models.IntegerField(blank=True, null=True)
    division = models.CharField(max_length=255, blank=True, null=True)
    absence = models.CharField(max_length=255, blank=True, null=True)
    possub = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'student_results'
        managed = False


class Student(models.Model):
    roll = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    madrasha = models.CharField(max_length=255)
    mid = models.CharField(max_length=255)
    class_name = models.CharField(max_length=255)
    sublabel_1 = models.CharField(max_length=255)
    subvalue_1 = models.CharField(max_length=255)
    sublabel_2 = models.CharField(max_length=255)
    subvalue_2 = models.CharField(max_length=255)
    sublabel_3 = models.CharField(max_length=255)
    subvalue_3 = models.CharField(max_length=255)
    sublabel_4 = models.CharField(max_length=255)
    subvalue_4 = models.CharField(max_length=255)
    sublabel_5 = models.CharField(max_length=255)
    subvalue_5 = models.CharField(max_length=255)
    sublabel_6 = models.CharField(max_length=255)
    subvalue_6 = models.CharField(max_length=255)
    sublabel_7 = models.CharField(max_length=255)
    subvalue_7 = models.CharField(max_length=255)
    sublabel_8 = models.CharField(max_length=255)
    subvalue_8 = models.CharField(max_length=255)
    sublabel_9 = models.CharField(max_length=255)
    subvalue_9 = models.CharField(max_length=255)
    sublabel_10 = models.CharField(max_length=255)
    subvalue_10 = models.CharField(max_length=255)
    sublabel_11 = models.CharField(max_length=255)
    subvalue_11 = models.CharField(max_length=255)
    total = models.CharField(max_length=255)
    gracelabel = models.CharField(max_length=255)
    gracevalue = models.CharField(max_length=255)
    positions = models.CharField(max_length=255)
    division = models.CharField(max_length=255)
    markaj = models.CharField(max_length=255)
    marid = models.CharField(max_length=255)
    srtype = models.BigIntegerField()
    melhaq = models.CharField(max_length=255)
    cid = models.BigIntegerField()
    father = models.CharField(max_length=255)
    dateofbirth = models.DateField()
    absence = models.CharField(max_length=255)
    possub = models.CharField(max_length=255)
    ids = models.CharField(max_length=255)
    years = models.BigIntegerField()
    reg_id = models.BigIntegerField()
    type = models.CharField(max_length=255)
    numbertoword = models.CharField(max_length=255)
    id = models.BigIntegerField()
    group_id = models.CharField(max_length=255)
    full_years = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    madrasha_bn = models.CharField(max_length=255)
    markaj_bn = models.CharField(max_length=255)
    passing_year = models.CharField(max_length=255)
    r_eregular = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    marhala_id = models.IntegerField()

    class Meta:
        db_table = 'students'
        managed = False


class student_adresss(models.Model):
    id = models.BigIntegerField(primary_key=True)
    student_id = models.BigIntegerField()
    division = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    thana = models.CharField(max_length=255, blank=True, null=True)
    post_office = models.CharField(max_length=255, blank=True, null=True)
    passport_photo = models.CharField(max_length=255, blank=True, null=True)
    birth_certificate_no = models.CharField(max_length=255, blank=True, null=True)
    birth_certificate_photo = models.CharField(max_length=255, blank=True, null=True)
    nid_no = models.CharField(max_length=255, blank=True, null=True)
    nid_photo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'student_adresss'
        managed = False


class student_attachment(models.Model):
    id = models.IntegerField(primary_key=True)
    student_id = models.IntegerField()
    birth_no = models.CharField(max_length=255, blank=True, null=True)
    birth_attach = models.CharField(max_length=255, blank=True, null=True)
    nid_no = models.CharField(max_length=255, blank=True, null=True)
    nid_attach = models.CharField(max_length=255, blank=True, null=True)
    marksheet = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'student_attachment'
        managed = False
