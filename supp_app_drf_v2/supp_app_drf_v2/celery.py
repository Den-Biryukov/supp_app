import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supp_app_drf_v2.settings')

app = Celery('supp_app_drf_v2')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# app.conf.beat_schedule = {
#     'send-mail-everyday-day-at-9.00am-(UTC+3)': {
#         'task': 'support.tasks.send_beat_mail_tickets',
#         'schedule': crontab(minute=0, hour=6),
#     },
# }

app.conf.beat_schedule = {
    'send-mail-everyday-minute': {
        'task': 'support.tasks.send_beat_mail_tickets',
        'schedule': crontab(),
    },
}
