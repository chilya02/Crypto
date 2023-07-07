import os
from celery import Celery
from celery.schedules import timedelta


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crypto.settings')

app = Celery('crypto')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'courses': {
        'task': 'courses.tasks.send_courses',
        'schedule': timedelta(seconds=2),
    }
}
