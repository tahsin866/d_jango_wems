from django.db import models


class ExamSetup(models.Model):
    """কেন্দ্রীয় পরীক্ষা সেটআপ মডেল - exam_setups table"""
    
    exam_name = models.CharField(
        max_length=255, 
        verbose_name="পরীক্ষার নাম"
    )
    arabic_year = models.CharField(
        max_length=100, 
        verbose_name="আরবি বছর"
    )
    bangla_year = models.CharField(
        max_length=100, 
        verbose_name="বাংলা বছর"
    )
    english_year = models.CharField(
        max_length=100, 
        verbose_name="ইংরেজি বছর"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="তৈরির তারিখ"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="আপডেটের তারিখ"
    )

    class Meta:
        db_table = 'exam_setups'
        verbose_name = 'কেন্দ্রীয় পরীক্ষা সেটআপ'
        verbose_name_plural = 'কেন্দ্রীয় পরীক্ষা সেটআপসমূহ'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.exam_name} - {self.bangla_year}"