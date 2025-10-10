from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.db import connection
import bcrypt

User = get_user_model()

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None
            
        user = None
        with connection.cursor() as cursor:
            try:
                cursor.execute("""
                    SELECT u.id, u.email, u.phone, u.password, ut.name as user_type, 
                           u.status, u.name, ac.name as admin_category, u.department_id
                    FROM users u
                    LEFT JOIN user_types ut ON u.user_type_id = ut.id
                    LEFT JOIN admin_categories ac ON u.admin_category_id = ac.id
                    WHERE LOWER(u.email) = LOWER(%s) OR u.phone = %s
                """, [username, username])
                row = cursor.fetchone()
                if row:
                    user_id, email, phone, db_password, user_type, status, name, admin_category, department_id = row
                    
                    if status != 'active':
                        return None
                    
                    # Check password - try both Django hash and bcrypt
                    password_valid = False
                    
                    # First try Django password hash (for new users from signup)
                    if db_password.startswith('pbkdf2_'):
                        password_valid = check_password(password, db_password)
                    else:
                        # Fallback to bcrypt for existing users
                        try:
                            password_valid = bcrypt.checkpw(password.encode('utf-8'), db_password.encode('utf-8'))
                        except:
                            password_valid = False
                    
                    if password_valid:
                        # Create or get Django user
                        try:
                            user = User.objects.get(email=email)
                        except User.DoesNotExist:
                            # Create new Django user based on custom users table data
                            user = User.objects.create_user(
                                username=email or phone,
                                email=email,
                                password=password
                            )
                        
                        # Store user info in session (session-based auth only)
                        if request is not None:
                            request.session['user_type'] = user_type
                            request.session['user_id'] = user_id
                            request.session['admin_category'] = admin_category
                            request.session['department_id'] = department_id

                        # Attach user info to user object
                        from apps.users.models import UserType, AdminCategory
                        # Always assign user_type as UserType instance
                        if isinstance(user_type, str):
                            try:
                                user.user_type = UserType.objects.get(name=user_type)
                            except UserType.DoesNotExist:
                                user.user_type = None
                        else:
                            user.user_type = user_type
                        # Always assign admin_category as AdminCategory instance
                        if isinstance(admin_category, str):
                            try:
                                user.admin_category = AdminCategory.objects.get(name=admin_category)
                            except AdminCategory.DoesNotExist:
                                user.admin_category = None
                        else:
                            user.admin_category = admin_category
                        user.custom_user_id = user_id
                        return user
            except Exception as e:
                print(f"Authentication error: {e}")
                return None
        return None
