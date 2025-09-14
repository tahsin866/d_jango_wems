from django.contrib import admin
from .models import ExamSetup


@admin.register(ExamSetup)
class ExamSetupAdmin(admin.ModelAdmin):
    """কেন্দ্রীয় পরীক্ষা সেটআপ অ্যাডমিন"""
    
    list_display = [
        'id', 
        'exam_name', 
        'bangla_year', 
        'english_year', 
        'arabic_year',
        'created_at'
    ]
    list_filter = ['bangla_year', 'english_year', 'created_at']
    search_fields = ['exam_name', 'bangla_year', 'english_year']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('পরীক্ষার তথ্য', {
            'fields': ('exam_name',)
        }),
        ('বছরের তথ্য', {
            'fields': ('arabic_year', 'bangla_year', 'english_year')
        }),
        ('টাইমস্ট্যাম্প', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )