from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    head_user_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'departments'
        managed = True


# Import existing models from users app to avoid conflicts
from apps.users.models import Module, Menu, Permission


# UserMenuPermission model commented out as table doesn't exist in database
# class UserMenuPermission(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
#     permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = 'user_menu_permissions'
#         managed = True
#         unique_together = ['user', 'menu', 'permission']