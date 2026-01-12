from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from celery.schedules import crontab
import json

class Command(BaseCommand):
    help = 'Set up periodic tasks for the application'

    def handle(self, *args, **options):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.minutes,
        )

        PeriodicTask.objects.update_or_create(
            name='Delete completed tasks every evening',
            defaults={
                'task': 'todos.tasks.delete_completed_tasks',
                'interval': schedule,
                'crontab': crontab(hour=18, minute=0),  # 6 PM daily
            }
        )

        self.stdout.write(self.style.SUCCESS('Successfully set up periodic tasks'))
