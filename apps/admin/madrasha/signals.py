from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.conf import settings

from apps.school.models import School


@receiver(post_save, sender=School)
def clear_madrasha_cache_on_save(sender, instance, **kwargs):
    """Clear madrasha cache when a School instance is saved"""
    from .views import MadrashaListView
    print(f"Clearing madrasha cache due to School save: {instance.id}")
    MadrashaListView.clear_cache()


@receiver(post_delete, sender=School)
def clear_madrasha_cache_on_delete(sender, instance, **kwargs):
    """Clear madrasha cache when a School instance is deleted"""
    from .views import MadrashaListView
    print(f"Clearing madrasha cache due to School delete: {instance.id}")
    MadrashaListView.clear_cache()