#!/bin/bash
python manage.py makemigrations
python manage.py migrate --noinput
python manage.py makesuperuser
python manage.py collectstatic --noinput

if [ "$RUN_CELERY" = "true" ]; then
    celery -A "todoApp.celery" worker -E -l info
elif [ "$RUN_CELERY_BEAT" = "true" ]; then
    celery -A "todoApp.celery" beat -l info
else
    # python manage.py makemigrations
    # python manage.py migrate
    
    python manage.py runserver 0.0.0.0:8000
fi
