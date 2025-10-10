from django.contrib import admin
from .models import Marhala, MarhalaSubject


@admin.register(Marhala)
class MarhalaAdmin(admin.ModelAdmin):
    """মারহালা অ্যাডমিন"""
    list_display = ['id', 'marhala_name_bn', 'marhala_name_en', 'marhala_name_ar', 'created_at']
    list_filter = ['created_at']
    search_fields = ['marhala_name_bn', 'marhala_name_en', 'marhala_name_ar']
    ordering = ['id']
    
    fieldsets = (
        ('মূল তথ্য', {
            'fields': ('marhala_name_bn', 'marhala_name_en', 'marhala_name_ar')
        }),
    )


@admin.register(MarhalaSubject)
class MarhalaSubjectAdmin(admin.ModelAdmin):
    """মারহালা সাবজেক্ট অ্যাডমিন"""
    list_display = [
        'id', 'marhala_id', 'name_bangla', 'subject_code', 
        'status', 'created_at'
    ]
    list_filter = ['marhala_id', 'status', 'created_at']
    search_fields = ['name_bangla', 'name_english', 'name_arabic', 'subject_code']
    list_editable = ['status']
    ordering = ['marhala_id', 'name_bangla']
    
    fieldsets = (
        ('মূল তথ্য', {
            'fields': ('marhala_id', 'name_bangla', 'name_english', 'name_arabic', 'subject_code')
        }),
        ('স্ট্যাটাস', {
            'fields': ('status',)
        }),
    )
