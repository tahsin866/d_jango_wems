from django.apps import AppConfig


class MadrashaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.admin.madrasha'
    verbose_name = 'Madrasha Management'

    def ready(self):
        """Import signals when the app is ready"""
        import apps.admin.madrasha.signals