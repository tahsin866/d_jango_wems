#!/usr/bin/env python
"""
Sample exam setups data creation script
"""
import os
import sys
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mysite.apps.CentralExam.models import ExamSetup

def create_sample_data():
    """Sample exam setups তৈরি করে"""
    
    sample_exams = [
        {
            'exam_name': '৫৭ তম পেন্নায় পরীক্ষা',
            'arabic_year': '১৪৪৭',
            'bangla_year': '১৪৩২',
            'english_year': '২০২৫'
        },
        {
            'exam_name': '৫৮ তম বার্ষিক পরীক্ষা',
            'arabic_year': '১৪৪৮',
            'bangla_year': '১৪৩৩',
            'english_year': '২০২৬'
        },
        {
            'exam_name': '৫৯ তম সেমিস্টার পরীক্ষা',
            'arabic_year': '১৪৪৯',
            'bangla_year': '১৪৩৪',
            'english_year': '২০২৭'
        },
        {
            'exam_name': '৬০ তম বিশেষ পরীক্ষা',
            'arabic_year': '১৪৫০',
            'bangla_year': '১৪৩৫',
            'english_year': '২০২৮'
        },
        {
            'exam_name': '৬১ তম নতুন বর্ষ পরীক্ষা',
            'arabic_year': '১৪৫১',
            'bangla_year': '১৪৩৬',
            'english_year': '২০২৯'
        }
    ]
    
    created_count = 0
    
    for exam_data in sample_exams:
        # Check if exam already exists
        if not ExamSetup.objects.filter(exam_name=exam_data['exam_name']).exists():
            exam = ExamSetup.objects.create(**exam_data)
            print(f"✅ Created: {exam.exam_name}")
            created_count += 1
        else:
            print(f"⚠️  Already exists: {exam_data['exam_name']}")
    
    print(f"\n🎉 Total {created_count} new exam setups created!")
    print(f"📊 Total exam setups in database: {ExamSetup.objects.count()}")
    
    # Display all exams
    print("\n📋 All Exam Setups in Database:")
    print("-" * 50)
    for exam in ExamSetup.objects.all().order_by('-created_at'):
        print(f"ID: {exam.id} | {exam.exam_name} | {exam.arabic_year}/{exam.english_year}")

if __name__ == '__main__':
    create_sample_data()