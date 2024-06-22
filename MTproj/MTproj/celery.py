from __future__ import absolute_import
import os
import time
from celery import Celery  # Corrected import here
from django.conf import settings
# I wrote this code

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MTproj.settings")
app = Celery("MTproj", broker="redis://localhost/", backend="redis://localhost/")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
# end of code I wrote
