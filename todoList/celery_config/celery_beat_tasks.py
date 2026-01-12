from celery import Celery
from celery.schedules import crontab


app = Celery('todApp')

#app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'delete-completed-todos-every-evening': {
        'task': 'todoList.tasks.delete_completed_todos',
        'schedule': crontab(hour=0, minute=0), # midnight
        'options': {'queue': 'default'},
    },
}

#app.conf.timezone = 'UTC'
