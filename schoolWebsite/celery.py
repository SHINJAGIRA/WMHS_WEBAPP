import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolWebsite.settings')

app = Celery('schoolWebsite')

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
app.conf.broker_url = 'redis://redis:6379/0'
app.conf.result_backend = 'redis://redis:6379/0'

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
