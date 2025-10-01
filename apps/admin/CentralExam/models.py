# models.py - FIXED VERSION
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
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.exam_name} - {self.bangla_year}"


class ExamFee(models.Model):
    """পরীক্ষার ফি মডেল - ✅ একটি মাত্র ডেফিনিশন"""
    
    # ✅ Foreign Key Relations - Correct
    exam_setup = models.ForeignKey(
        ExamSetup, 
        on_delete=models.CASCADE, 
        related_name='fees',
        verbose_name="পরীক্ষা সেটআপ",
        null=False,  # Required
        blank=False  # Required in forms
    )
    
    marhala = models.ForeignKey(
        'subject.Marhala',  # ✅ App reference দিয়ে
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='exam_fees',
        verbose_name="মারহালা"
    )
    
    # ✅ Regular Fee Fields
    reg_date_from = models.DateField(null=True, blank=True, verbose_name="নিয়মিত ফি শুরুর তারিখ")
    reg_date_to = models.DateField(null=True, blank=True, verbose_name="নিয়মিত ফি শেষের তারিখ")
    reg_regular_fee = models.DecimalField(
        max_digits=10, decimal_places=2, 
        null=True, blank=True, 
        verbose_name="নিয়মিত ফি"
    )
    reg_irregular_jemni = models.DecimalField(
        max_digits=10, decimal_places=2, 
        null=True, blank=True,
        verbose_name="অনিয়মিত জেমনি ফি"
    )
    reg_irregular_manonnoyon = models.DecimalField(
        max_digits=10, decimal_places=2, 
        null=True, blank=True,
        verbose_name="অনিয়মিত মনোনয়ন ফি"
    )
    reg_irregular_others = models.DecimalField(
        max_digits=10, decimal_places=2, 
        null=True, blank=True,
        verbose_name="অনিয়মিত অন্যান্য ফি"
    )
    
    # ✅ Late Fee Fields
    late_date_from = models.DateField(null=True, blank=True, verbose_name="বিলম্ব ফি শুরুর তারিখ")
    late_date_to = models.DateField(null=True, blank=True, verbose_name="বিলম্ব ফি শেষের তারিখ")
    late_regular_fee = models.DecimalField(
        max_digits=10, decimal_places=2, 
        null=True, blank=True,
        verbose_name="বিলম্ব নিয়মিত ফি"
    )
    late_irregular_jemni = models.DecimalField(
        max_digits=10, decimal_places=2, 
        null=True, blank=True,
        verbose_name="বিলম্ব অনিয়মিত জেমনি ফি"
    )
    late_irregular_manonnoyon = models.DecimalField(
        max_digits=10, decimal_places=2, 
        null=True, blank=True,
        verbose_name="বিলম্ব অনিয়মিত মনোনয়ন ফি"
    )
    late_irregular_others = models.DecimalField(
        max_digits=10, decimal_places=2, 
        null=True, blank=True,
        verbose_name="বিলম্ব অনিয়মিত অন্যান্য ফি"
    )
    
    # ✅ Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="তৈরির তারিখ")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="আপডেটের তারিখ")

    class Meta:
        db_table = 'exam_fees'
        verbose_name = 'পরীক্ষার ফি'
        verbose_name_plural = 'পরীক্ষার ফিসমূহ'
        ordering = ['exam_setup', 'marhala']
        # ✅ Unique constraint যাতে একই setup এর জন্য একই marhala এর ফি দুইবার না হয়
        unique_together = ['exam_setup', 'marhala']

    def __str__(self):
        marhala_name = self.marhala.name if self.marhala else "সব মারহালা"
        return f"{self.exam_setup.exam_name} - {marhala_name}"