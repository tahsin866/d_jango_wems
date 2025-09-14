#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mysite.apps.subject.models import SubjectSettings

# Check existing data
print("=== Checking SubjectSettings data ===")
settings = SubjectSettings.objects.all()

if settings.exists():
    for setting in settings[:5]:  # Show first 5 records
        print(f"ID: {setting.id}")
        print(f"Subject Names: {setting.subject_names}")
        print(f"Subject Type: '{setting.subject_type}' (type: {type(setting.subject_type)})")
        print(f"Student Type: '{setting.student_type}' (type: {type(setting.student_type)})")
        print(f"Marhala Type: '{setting.marhala_type}'")
        print(f"Status: '{setting.status}'")
        print("-" * 50)
else:
    print("No SubjectSettings data found!")

print(f"Total records: {settings.count()}")