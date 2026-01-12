from celery import shared_task
from .models import TODO
from django.utils import timezone

@shared_task(bind=True)
def delete_completed_todos(*args, **kwargs):
    print('Deleting')
    results=TODO.objects.filter(status='c', date__lt=timezone.now()).delete()
    print(f'Deleted {results[0]} completed tasks')
