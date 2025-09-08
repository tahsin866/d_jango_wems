from django.db import models

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
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('disabled', 'Disabled'),
    ]
    
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=200)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)
    admin_category = models.ForeignKey(AdminCategory, on_delete=models.CASCADE, null=True, blank=True)
    registration_no = models.CharField(max_length=50, blank=True)
    roll_no = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name

class UserInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='information')
    madrasha_id = models.IntegerField(null=True, blank=True)  # schools table এর id (primary key) বসবে এখানে
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

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_roles'