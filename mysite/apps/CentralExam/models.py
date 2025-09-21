from django.db import models

class ExamSetup(models.Model):
    """কেন্দ্রীয় পরীক্ষা সেটআপ মডেল"""
    exam_name = models.CharField(max_length=255, verbose_name="পরীক্ষার নাম")
    arabic_year = models.CharField(max_length=100, verbose_name="আরবি বছর")
    bangla_year = models.CharField(max_length=100, verbose_name="বাংলা বছর")
    english_year = models.CharField(max_length=100, verbose_name="ইংরেজি বছর")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="তৈরির তারিখ")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="আপডেটের তারিখ")

    class Meta:
        db_table = 'exam_setups'
        verbose_name = 'কেন্দ্রীয় পরীক্ষা সেটআপ'
        verbose_name_plural = 'কেন্দ্রীয় পরীক্ষা সেটআপসমূহ'
        ordering = ['-created_at']  # সর্বশেষ তৈরি আগে


    def __str__(self):
        return f"{self.exam_name} - {self.bangla_year}"


class ExamFee(models.Model):
    exam_setup = models.ForeignKey(ExamSetup, on_delete=models.CASCADE, related_name='fees', null=True, blank=True)
    # Add marhala_id ForeignKey
    marhala = models.ForeignKey('subject.Marhala', on_delete=models.SET_NULL, null=True, blank=True, related_name='exam_fees')
    reg_date_from = models.DateField(null=True, blank=True)
    reg_date_to = models.DateField(null=True, blank=True)
    reg_regular_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reg_irregular_jemni = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reg_irregular_manonnoyon = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reg_irregular_others = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    late_date_from = models.DateField(null=True, blank=True)
    late_date_to = models.DateField(null=True, blank=True)
    late_regular_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    late_irregular_jemni = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    late_irregular_manonnoyon = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    late_irregular_others = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'exam_fees'
        verbose_name = 'Exam Fee'
        verbose_name_plural = 'Exam Fees'
        ordering = ['id']

    def __str__(self):
        return f"ExamFee ({self.exam_setup_id})"