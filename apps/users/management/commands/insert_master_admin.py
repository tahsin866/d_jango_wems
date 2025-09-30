from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from users.models import Module, Menu

from django.db import connection

def insert_master_admin():
    with connection.cursor() as cursor:
        # Insert user_types
        cursor.execute("""
            INSERT INTO user_types (name, description) VALUES
            ('Admin', 'System Admin'),
            ('Madrasah', 'Madrasah User'),
            ('Markaz', 'Markaz User'),
            ('Negaran', 'Negaran User'),
            ('Mumtahin', 'Mumtahin User'),
            ('Zonal', 'Zonal User'),
            ('Student', 'Student User')
            ON CONFLICT DO NOTHING;
        """)
        # Insert admin_categories
        cursor.execute("""
            INSERT INTO admin_categories (name, description) VALUES
            ('Master Admin', 'Full access'),
            ('Super Admin', 'Super access'),
            ('Board Admin', 'Board access'),
            ('Admin', 'General admin')
            ON CONFLICT DO NOTHING;
        """)
        # Get ids
        cursor.execute("SELECT id FROM user_types WHERE name='Admin'")
        user_type_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM admin_categories WHERE name='Master Admin'")
        admin_category_id = cursor.fetchone()[0]
        # Insert master admin user
        cursor.execute("""
            INSERT INTO users (name, phone, email, password, user_type_id, admin_category_id, status, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, [
            'Master Admin',
            '01700000000',
            'masteradmin@example.com',
            'pbkdf2_sha256$260000$dummy$dummyhash', # Change to real hash
            user_type_id,
            admin_category_id,
            'active',
            timezone.now(),
            timezone.now()
        ])

class Command(BaseCommand):
    help = 'Insert master admin and required initial data'

    def handle(self, *args, **options):
        with transaction.atomic():
            insert_master_admin()
        self.stdout.write(self.style.SUCCESS('Master admin and initial data inserted.'))
