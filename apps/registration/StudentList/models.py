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
    def marhala_name(self):
        """Get marhala name from marhala_id"""
        # Add marhala mapping logic here when marhala model is available
        marhala_mapping = {
            1: 'ইবতেদাইয়্যাহ',
            2: 'মুতাওয়াসসিতা',
            3: 'সানাবিয়া',
            4: 'সানাবিয়া উলইয়া',
            5: 'ফযীলত',
            6: 'হিফজুল কোরান',
            7: 'কিরাআত',
        }
        return marhala_mapping.get(self.marhala_id, 'অজানা')

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