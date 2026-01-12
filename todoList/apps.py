from django.apps import AppConfig


class TodolistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todoList'

    def ready(self) -> None:
        from todoList import tasks
        from todoList.celery_config import celery_beat_tasks
        return super().ready()
