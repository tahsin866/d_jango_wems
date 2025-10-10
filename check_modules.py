#!/usr/bin/env python
"""
Quick script to check modules and menus in database
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.db import connection

def check_modules_and_menus():
    with connection.cursor() as cursor:
        # Check modules with department info
        print("\n" + "="*70)
        print("MODULES WITH DEPARTMENT INFO")
        print("="*70)
        cursor.execute("""
            SELECT m.id, m.name, m.department_id, d.name as dept_name, COUNT(mn.id) as menu_count
            FROM modules m
            LEFT JOIN departments d ON m.department_id = d.id
            LEFT JOIN menus mn ON m.id = mn.module_id
            GROUP BY m.id, m.name, m.department_id, d.name
            ORDER BY m.id
        """)
        
        modules = cursor.fetchall()
        if not modules:
            print("❌ No modules found in database!")
        else:
            for row in modules:
                mod_id, mod_name, dept_id, dept_name, menu_count = row
                dept_info = f"Dept: {dept_id} ({dept_name})" if dept_id else "Dept: NULL (Global)"
                print(f"  Module {mod_id}: {mod_name:30} | {dept_info:30} | Menus: {menu_count}")
        
        # Check total menus
        print("\n" + "="*70)
        print("TOTAL COUNTS")
        print("="*70)
        cursor.execute("SELECT COUNT(*) FROM modules")
        total_modules = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM menus")
        total_menus = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM departments")
        total_depts = cursor.fetchone()[0]
        
        print(f"  Total Modules: {total_modules}")
        print(f"  Total Menus: {total_menus}")
        print(f"  Total Departments: {total_depts}")
        
        # Check users with departments
        print("\n" + "="*70)
        print("USERS WITH DEPARTMENTS")
        print("="*70)
        cursor.execute("""
            SELECT u.id, u.name, u.email, u.department_id, d.name as dept_name
            FROM users u
            LEFT JOIN departments d ON u.department_id = d.id
            ORDER BY u.id
            LIMIT 10
        """)
        
        users = cursor.fetchall()
        if not users:
            print("❌ No users found!")
        else:
            for row in users:
                user_id, user_name, user_email, dept_id, dept_name = row
                dept_info = f"Dept: {dept_id} ({dept_name})" if dept_id else "No Department"
                print(f"  User {user_id}: {user_name:20} | {user_email:30} | {dept_info}")

if __name__ == '__main__':
    check_modules_and_menus()
