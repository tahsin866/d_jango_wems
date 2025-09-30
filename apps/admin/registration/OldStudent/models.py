from django.db import models

class student_basic(models.Model):
    id = models.AutoField(primary_key=True)
    photo = models.CharField(max_length=255, blank=True, null=True)
    student_name_bn = models.CharField(max_length=255)
    student_name_ar = models.CharField(max_length=255, blank=True, null=True)
    student_name_en = models.CharField(max_length=255, blank=True, null=True)
    father_name_bn = models.CharField(max_length=255)
    father_name_ar = models.CharField(max_length=255, blank=True, null=True)
    father_name_en = models.CharField(max_length=255, blank=True, null=True)
    mother_name_bn = models.CharField(max_length=255, blank=True, null=True)
    mother_name_ar = models.CharField(max_length=255, blank=True, null=True)
    mother_name_en = models.CharField(max_length=255, blank=True, null=True)
    roll_no = models.IntegerField()
    reg_no = models.CharField(max_length=255)
    year = models.IntegerField()
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
