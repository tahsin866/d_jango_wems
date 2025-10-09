
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
    madrasa_id = models.IntegerField(null=True, blank=True)  # user_information.madrasha_id এর ডাটা বসবে
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
    madrasa_id = models.IntegerField(null=True, blank=True)  # user_information.madrasha_id এর ডাটা বসবে
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

# Centers টেবিল
class Center(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'centers'
        managed = False  # Database table already exists

    def __str__(self):
        return self.name or f"Center {self.id}"

# Madrasha Centers টেবিল
class MadrashaCenter(models.Model):
    id = models.BigAutoField(primary_key=True)
    madrasha_id = models.CharField(max_length=100, null=True, blank=True)  # schools.school_id reference
    center_id = models.BigIntegerField(null=True, blank=True)  # centers.id reference
    serial_number = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'madrasha_centers'
        managed = False  # Database table already exists

    def __str__(self):
        return f"Madrasha {self.madrasha_id} - Center {self.center_id}"

# Madrasha Under Centers টেবিল
class MadrashaUnderCenter(models.Model):
    id = models.BigAutoField(primary_key=True)
    parent_madrasha_id = models.CharField(max_length=100, null=True, blank=True)  # schools.school_id reference
    center_id = models.BigIntegerField(null=True, blank=True)  # centers.id reference
    child_madrasha_id = models.CharField(max_length=100, null=True, blank=True)  # schools.school_id reference
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'madrasha_under_centers'
        managed = False  # Database table already exists

    def __str__(self):
        return f"Parent {self.parent_madrasha_id} - Child {self.child_madrasha_id} - Center {self.center_id}"



