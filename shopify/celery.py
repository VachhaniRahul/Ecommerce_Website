# project_name/celery.py
import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopify.settings')

app = Celery('shopify')

# Load settings from Django settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')


# Auto-discover tasks in Django apps
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'send-email-every-5-minutes': {
#         'task': 'base.emails.send_profile_activation_email',
#         'schedule': crontab(minute='*/1'),  # Runs every 5 minutes
#         'args': ('rahul.vachhani@openxcell.com', '123456'),  # Replace with actual email & token
#     },
# }

