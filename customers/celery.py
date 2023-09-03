from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "R4C.settings")
app = Celery("customers", broker_connection_retry_on_startup=True)
app.config_from_object("django.conf:settings", namespace="CELERY")