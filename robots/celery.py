import os
from datetime import datetime, timedelta

from celery import Celery
from celery.schedules import crontab

from robots.tasks import generate_report

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'R4C.settings')
app = Celery('robots', backend="redis", broker_connection_retry_on_startup=True)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'Europe/Moscow'


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour="0", minute="0"),
        generate_report.s(datetime.now() - timedelta(days=7), datetime.now()),
    )




