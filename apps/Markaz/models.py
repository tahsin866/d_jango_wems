
from django.db import models
from apps.users.models import User
from apps.admin.CentralExam.models import ExamSetup
from apps.school.models import School

class MarkazApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(ExamSetup, on_delete=models.SET_NULL, null=True)
    markaz_type = models.CharField(max_length=64)
    requirements = models.TextField(default='0')
    status = models.CharField(max_length=32, default='pending')
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    printed = models.BooleanField(default=False)
    printed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'markaz_applications'

class MainMadrasaInfo(models.Model):
    markaz_application = models.ForeignKey(MarkazApplication, on_delete=models.CASCADE)
    madrasa = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    fazilat = models.IntegerField(blank=True, null=True)
    sanabiya_ulya = models.IntegerField(blank=True, null=True)
    sanabiya = models.IntegerField(blank=True, null=True)
    mutawassita = models.IntegerField(blank=True, null=True)
    ibtedaiyyah = models.IntegerField(blank=True, null=True)
    hifzul_quran = models.IntegerField(blank=True, null=True)
    qirat = models.IntegerField(blank=True, null=True)
    noc_file_path = models.CharField(max_length=256, blank=True, null=True)
    resolution_file_path = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        db_table = 'main_madrasa_infos'

class AssociatedMadrasa(models.Model):
    markaz_application = models.ForeignKey(MarkazApplication, on_delete=models.CASCADE)
    madrasa = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    fazilat = models.IntegerField(blank=True, null=True)
    sanabiya_ulya = models.IntegerField(blank=True, null=True)
    sanabiya = models.IntegerField(blank=True, null=True)
    mutawassita = models.IntegerField(blank=True, null=True)
    ibtedaiyyah = models.IntegerField(blank=True, null=True)
    hifzul_quran = models.IntegerField(blank=True, null=True)
    qirat = models.IntegerField(blank=True, null=True)
    noc_file_path = models.CharField(max_length=256, blank=True, null=True)
    resolution_file_path = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        db_table = 'associated_madrasas'

class Attachment(models.Model):
    markaz_application = models.ForeignKey(MarkazApplication, on_delete=models.CASCADE)
    type = models.CharField(max_length=32)
    file_path = models.CharField(max_length=256)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'attachments'

class MarkazApplicationAudit(models.Model):
    markaz_application = models.ForeignKey(MarkazApplication, on_delete=models.CASCADE)
    action = models.CharField(max_length=64)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    status = models.CharField(max_length=32, blank=True, null=True)
    printed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'markaz_application_audit'



