from django.db import models

class Marhala(models.Model):
    """মারহালা মডেল - Existing Table"""
    marhala_name_bn = models.CharField(max_length=255, verbose_name="মারহালা নাম (বাংলা)")
    marhala_name_en = models.CharField(max_length=255, verbose_name="মারহালা নাম (ইংরেজি)", blank=True, null=True)
    marhala_name_ar = models.CharField(max_length=255, verbose_name="মারহালা নাম (আরবি)", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="তৈরির তারিখ")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="আপডেটের তারিখ")

    class Meta:
        db_table = 'marhalas'
        verbose_name = 'মারহালা'
        verbose_name_plural = 'মারহালাসমূহ'
        ordering = ['id']

    def __str__(self):
        return self.marhala_name_bn or self.marhala_name_en or str(self.id)

class MarhalaSubject(models.Model):
    """মারহালা সাবজেক্ট মডেল - Existing Table"""
    STATUS_CHOICES = [
        ('both', 'ছেলে ও মেয়ে উভয়'),
        ('SRtype_1', 'শুধু ছেলেদের'),
        ('SRtype_0', 'শুধু মেয়েদের'),
    ]
    marhala = models.ForeignKey(
        Marhala, 
        on_delete=models.CASCADE, 
        related_name='subjects',
        verbose_name="মারহালা"
    )
    subject_code = models.CharField(max_length=50, verbose_name="বিষয় কোড", blank=True, null=True)
    name_bangla = models.CharField(max_length=255, verbose_name="বিষয়ের নাম (বাংলা)")
    name_english = models.CharField(max_length=255, verbose_name="বিষয়ের নাম (ইংরেজি)", blank=True, null=True)
    name_arabic = models.CharField(max_length=255, verbose_name="বিষয়ের নাম (আরবি)", blank=True, null=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='both',
        verbose_name="স্ট্যাটাস"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="তৈরির তারিখ")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="আপডেটের তারিখ")

    class Meta:
        db_table = 'marhala_subjects'
        verbose_name = 'মারহালা সাবজেক্ট'
        verbose_name_plural = 'মারহালা সাবজেক্টসমূহ'
        ordering = ['marhala_id', 'name_bangla']

    def __str__(self):
        return f"{self.marhala.marhala_name_bn} - {self.name_bangla}"

class SubjectSettings(models.Model):
    """সাবজেক্ট সেটিংস মডেল - subject_settings table"""
    STUDENT_TYPE_CHOICES = [
        ('ছাত্র', 'ছাত্র'),
        ('ছাত্রী', 'ছাত্রী'),
        ('উভয়', 'উভয়'),
    ]
    SYLLABUS_TYPE_CHOICES = [
        ('আবশ্যিক', 'আবশ্যিক'),
        ('নৈর্বাচনিক', 'নৈর্বাচনিক'),
    ]
    MARKAZ_TYPE_CHOICES = [
        ('দরসিয়াত', 'দরসিয়াত'),
        ('হিফজুল কোরআন', 'হিফজুল কোরআন'),
        ('কিরাআত', 'কিরাআত'),
    ]
    SUBJECT_TYPE_CHOICES = [
        ('মিইয়ারী', 'মিইয়ারী'),
        ('গায়রে মি\'ইয়ারী', 'গায়রে মি\'ইয়ারী'),
    ]
    STATUS_CHOICES = [
        ('active', 'সক্রিয়'),
        ('inactive', 'নিষ্ক্রিয়'),
    ]
    marhala = models.ForeignKey(
        Marhala, 
        on_delete=models.CASCADE, 
        db_column='marhala_id',
        verbose_name="মারহালা"
    )
    subject = models.ForeignKey(
        MarhalaSubject, 
        on_delete=models.CASCADE, 
        db_column='subject_id',
        verbose_name="সাবজেক্ট"
    )
    marhala_type = models.CharField(max_length=100, verbose_name="মারহালার ধরন")
    subject_names = models.CharField(max_length=255, verbose_name="সাবজেক্টের নাম")
    student_type = models.CharField(
        max_length=50, 
        choices=STUDENT_TYPE_CHOICES,
        default='উভয়',
        verbose_name="শিক্ষার্থীর ধরন"
    )
    syllabus_type = models.CharField(
        max_length=50, 
        choices=SYLLABUS_TYPE_CHOICES,
        default='আবশ্যিক',
        verbose_name="সিলেবাসের ধরন"
    )
    markaz_type = models.CharField(
        max_length=100, 
        choices=MARKAZ_TYPE_CHOICES,
        default='দরসিয়াত',
        verbose_name="মারকাযের ধরন"
    )
    subject_type = models.CharField(
        max_length=50, 
        choices=SUBJECT_TYPE_CHOICES,
        default='মিইয়ারী',
        verbose_name="সাবজেক্টের ধরন"
    )
    total_marks = models.PositiveIntegerField(default=100, verbose_name="সর্বোচ্চ নম্বর")
    pass_marks = models.PositiveIntegerField(default=40, verbose_name="পাশের নম্বর")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='active',
        verbose_name="স্ট্যাটাস"
    )
    subject_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="সাবজেক্ট কোড")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="তৈরির তারিখ")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="আপডেটের তারিখ")

    class Meta:
        db_table = 'subject_settings'
        managed = True
        verbose_name = 'সাবজেক্ট সেটিংস'
        verbose_name_plural = 'সাবজেক্ট সেটিংসমূহ'
        ordering = ['marhala_id', 'subject_names']
        indexes = [
            models.Index(fields=['marhala_id'], name='subj_set_marhala_idx'),
            models.Index(fields=['status'], name='subj_set_status_idx'),
            models.Index(fields=['markaz_type'], name='subj_set_markaz_idx'),
            models.Index(fields=['student_type'], name='subj_set_student_idx'),
            models.Index(fields=['marhala_id', 'status'], name='subj_set_mar_stat_idx'),
        ]

    def __str__(self):
        return f"{self.marhala_type} - {self.subject_names}"