from django.apps import AppConfig


class AddressConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.address'
    verbose_name = 'Address Management'
    verbose_name_plural = 'Address Management'