from django.core.management.base import BaseCommand
from django.conf import settings
from apps.admin.subject.models import Marhala, MarhalaSubject, SubjectSettings
from apps.admin.subject.cache import SubjectCache

class Command(BaseCommand):
    help = 'Dump all subject app tables to Redis cache for zero-query serving.'

    def handle(self, *args, **kwargs):
        # Marhala table
        marhalas = list(Marhala.objects.all().values())
        SubjectCache.set_cache('all_marhalas', marhalas, timeout=getattr(settings, 'CACHE_TIMEOUT_LONG', 86400))
        self.stdout.write(self.style.SUCCESS(f'Marhala table cached: {len(marhalas)} rows'))

        # MarhalaSubject table
        subjects = list(MarhalaSubject.objects.all().values())
        SubjectCache.set_cache('all_marhala_subjects', subjects, timeout=getattr(settings, 'CACHE_TIMEOUT_LONG', 86400))
        self.stdout.write(self.style.SUCCESS(f'MarhalaSubject table cached: {len(subjects)} rows'))

        # SubjectSettings table
        settings_rows = list(SubjectSettings.objects.all().values())
        SubjectCache.set_cache('all_subject_settings', settings_rows, timeout=getattr(settings, 'CACHE_TIMEOUT_LONG', 86400))
        self.stdout.write(self.style.SUCCESS(f'SubjectSettings table cached: {len(settings_rows)} rows'))

        self.stdout.write(self.style.SUCCESS('All subject app tables cached in Redis!'))
