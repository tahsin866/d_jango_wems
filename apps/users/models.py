from django.db import models
from django.contrib.auth import get_user_model
class UserType(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'user_types'

    def __str__(self):
        return self.name

class AdminCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'admin_categories'

    def __str__(self):
        return self.name

class User(models.Model):
    # --- Django authentication compatibility ---
    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    # --- Password check method for authentication ---
    from django.contrib.auth.hashers import check_password as django_check_password
    def check_password(self, raw_password):
        return self.django_check_password(raw_password, self.password)

    # --- Note for user_type assignment ---
    # Always assign user_type as UserType instance, not string.
    # Example: user.user_type = UserType.objects.get(name='Master Admin')
    # Django custom user model requirements
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']
    from django.contrib.auth.models import UserManager
    objects = UserManager()
    last_login = models.DateTimeField(null=True, blank=True)

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('disabled', 'Disabled'),
    ]

        # Remove last_login property to avoid setter error

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=200)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)
    admin_category = models.ForeignKey(AdminCategory, on_delete=models.CASCADE, null=True, blank=True)
    department_id = models.IntegerField(null=True, blank=True)  # Department foreign key
    registration_no = models.CharField(max_length=50, blank=True)
    roll_no = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

class UserInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='information')
    madrasha_id = models.IntegerField(null=True, blank=True)  # schools table এর id (primary key) বসবে এখানে
    school_id = models.IntegerField(null=True, blank=True)  # schools table এর id (primary key) থেকে আসবে
    custom_code = models.CharField(max_length=50, blank=True)  # registration code
    admin_designation = models.CharField(max_length=100, blank=True)  # এডমিনের পদবি
    nid_no = models.CharField(max_length=20, blank=True)  # জাতীয় পরিচয়পত্র নম্বর
    whatsapp_no = models.CharField(max_length=20, blank=True, null=True)  # হোয়াটস এপ নম্বর (existing column name)
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True)  # পাসপোর্ট সাইজের ছবি
    nid_photo = models.ImageField(upload_to='nid_photos/', blank=True, null=True)  # ভোটার আইডি কার্ডের ছবি
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_information'
        managed = False  # Since table already exists

    def __str__(self):
        return f"{self.user.name} - Information"

class Module(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    icon = models.CharField(max_length=100, blank=True, default='SettingsIcon')
    department_id = models.IntegerField(null=True, blank=True)  # Link to departments table

    class Meta:
        db_table = 'modules'

    def __str__(self):
        return self.name

class Menu(models.Model):
    module = models.ForeignKey(Module, related_name='menus', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    href = models.CharField(max_length=200, blank=True)
    icon = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'menus'

    def __str__(self):
        return f"{self.module.name} - {self.name}"

class Permission(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'permissions'

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=50)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE, null=True, blank=True)
    admin_category = models.ForeignKey(AdminCategory, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.name

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        db_table = 'role_permissions'


    class Meta:
        db_table = 'user_roles'

# ------------------ Custom User Activity Models ------------------

class UserLoginHistory(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_histories')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    device = models.CharField(max_length=255, blank=True, null=True)
    browser = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        db_table = 'user_login_history'

class UserFailedAttempts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='failed_attempts')
    attempt_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    reason = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'user_failed_attempts'

class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=255)
    request_path = models.TextField(blank=True, null=True)
    meta_data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_activity_log'

class UserSessions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    device = models.CharField(max_length=255, blank=True, null=True)
    browser = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'user_sessions'

class UserTokens(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    token = models.TextField()
    issued_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    revoked = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_tokens'