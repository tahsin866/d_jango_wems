from django.db import models
from apps.admin.CentralExam.models import ExamSetup
from apps.school.models import School


class StudentBasic(models.Model):
    """
    Student Basic Information Model
    Maps to student_basic table
    """
    id = models.BigAutoField(primary_key=True)
    photo = models.CharField(max_length=255, null=True, blank=True)
    student_name_bn = models.CharField(max_length=255, null=True, blank=True)
    student_name_ar = models.CharField(max_length=255, null=True, blank=True)
    student_name_en = models.CharField(max_length=255, null=True, blank=True)
    father_name_bn = models.CharField(max_length=255, null=True, blank=True)
    father_name_ar = models.CharField(max_length=255, null=True, blank=True)
    father_name_en = models.CharField(max_length=255, null=True, blank=True)
    mother_name_bn = models.CharField(max_length=255, null=True, blank=True)
    mother_name_ar = models.CharField(max_length=255, null=True, blank=True)
    mother_name_en = models.CharField(max_length=255, null=True, blank=True)
    roll_no = models.IntegerField(null=True, blank=True)
    reg_no = models.IntegerField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    marhala_id = models.IntegerField(null=True, blank=True)
    cid = models.IntegerField(null=True, blank=True)
    srtype = models.IntegerField(null=True, blank=True)
    hijri_year = models.IntegerField(null=True, blank=True)
    bangla_year = models.IntegerField(null=True, blank=True)
    students_type = models.CharField(max_length=50, null=True, blank=True)
    exam_id = models.IntegerField(null=True, blank=True)
    madrasha_id = models.IntegerField(null=True, blank=True)
    markaz_id = models.IntegerField(null=True, blank=True)
    is_old = models.IntegerField(null=True, blank=True, default=0)
    irregular_sub = models.IntegerField(null=True, blank=True, default=0)

    
    class Meta:
        db_table = 'student_basic'
        managed = False  # This table already exists in database
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student_name_bn} ({self.reg_no})" if self.student_name_bn else f"Student {self.id}"

    @property
    def exam_name(self):
        """Get exam name from exam_id"""
        if self.exam_id:
            try:
                from apps.admin.CentralExam.models import ExamSetup
                exam = ExamSetup.objects.filter(id=self.exam_id).first()
                return exam.exam_name if exam else None
            except Exception:
                return None
        return None

    @property
    def madrasha_name(self):
        """Get madrasha name from madrasha_id"""
        if self.madrasha_id:
            try:
                from apps.school.models import School
                school = School.objects.filter(school_id=self.madrasha_id).first()
                return school.mname if school else None
            except Exception:
                return None
        return None

    @property
    def markaz_name(self):
        """Get markaz name from markaz_id"""
        if self.markaz_id:
            try:
                from apps.school.models import School
                school = School.objects.filter(school_id=self.markaz_id).first()
                return school.mname if school else None
            except Exception:
                return None
        return None

    @property
    def marhala_name(self):
        """Get marhala name from marhala_id"""
        if self.marhala_id:
            try:
                from apps.admin.subject.models import Marhala
                marhala = Marhala.objects.filter(id=self.marhala_id).first()
                return marhala.marhala_name_bn if marhala else None
            except Exception:
                return None
        return None

    @property
    def student_type_display(self):
        """Get student type display text"""
        if self.students_type:
            return "Female (ছাত্রী)" if str(self.students_type) == "0" else "Male (ছাত্র)"
        return None

    @property
    def payment_status(self):
        """Calculate payment status - this is a placeholder"""
        # Add payment status logic here when payment model is available
        return 'পেমেন্ট পেন্ডিং'

    @property
    def is_paid(self):
        """Check if payment is completed - this is a placeholder"""
        # Add payment check logic here when payment model is available
        return False

    @property
    def student_address(self):
        """Get student address from student_address table"""
        try:
            return StudentAddress.objects.filter(student_id=self.id).first()
        except Exception:
            return None

    @property
    def division_name(self):
        """Get division name from student address"""
        address = self.student_address
        if address and address.division:
            try:
                from apps.address.models import Division
                division_id = int(address.division) if address.division else None
                division = Division.objects.filter(id=division_id).first()
                return division.dname if division else None
            except Exception:
                return None
        return None

    @property
    def district_name(self):
        """Get district name from student address"""
        address = self.student_address
        if address and address.district:
            try:
                from apps.address.models import District
                district_id = int(address.district) if address.district else None
                district = District.objects.filter(id=district_id).first()
                return district.dname if district else None
            except Exception:
                return None
        return None

    @property
    def thana_name(self):
        """Get thana name from student address"""
        address = self.student_address
        if address and address.thana:
            try:
                from apps.address.models import Thana
                thana_id = int(address.thana) if address.thana else None
                thana = Thana.objects.filter(id=thana_id).first()
                return thana.dname if thana else None
            except Exception:
                return None
        return None


class StudentAddress(models.Model):
    """
    Student Address Information Model
    Maps to student_address table
    """
    student = models.OneToOneField(
        StudentBasic,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='student_id',
        verbose_name="Student"
    )
    division = models.CharField(max_length=10, null=True, blank=True, verbose_name="বিভাগ")
    district = models.CharField(max_length=10, null=True, blank=True, verbose_name="জেলা")
    thana = models.CharField(max_length=10, null=True, blank=True, verbose_name="থানা")
    post_office = models.CharField(max_length=255, null=True, blank=True, verbose_name="পোস্ট অফিস")
    passport_photo = models.CharField(max_length=255, null=True, blank=True, verbose_name="পাসপোর্ট ছবি")
    birth_certificate_no = models.CharField(max_length=100, null=True, blank=True, verbose_name="জন্ম সনদ নম্বর")
    birth_certificate_photo = models.CharField(max_length=255, null=True, blank=True, verbose_name="জন্ম সনদ ছবি")
    nid_no = models.CharField(max_length=50, null=True, blank=True, verbose_name="এনআইডি নম্বর")
    nid_photo = models.CharField(max_length=255, null=True, blank=True, verbose_name="এনআইডি ছবি")

    class Meta:
        db_table = 'student_address'
        managed = False  # This table already exists in database

    def __str__(self):
        return f"Address for {self.student.student_name_bn if self.student else 'Unknown'}"