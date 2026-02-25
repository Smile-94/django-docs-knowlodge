import os

from celery import Celery
from django.conf import settings

# ------------------------------------------------------------------------------
# Ensure Django settings are available before Celery initializes
# This is required so Celery can access Django settings, apps, and ORM
# ------------------------------------------------------------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


# ------------------------------------------------------------------------------
# Create the Celery application instance
# The name ("config") should match the Django project for consistency
# ------------------------------------------------------------------------------
app = Celery("config")


# ------------------------------------------------------------------------------
# Load Celery configuration from Django settings
# All Celery-related settings must be prefixed with `CELERY_`
# Example: CELERY_BROKER_URL, CELERY_ACCEPT_CONTENT, etc.
# ------------------------------------------------------------------------------
app.config_from_object("django.conf:settings", namespace="CELERY")


# ------------------------------------------------------------------------------
# Auto-discover tasks from all registered Django apps
# Celery will look for a `tasks.py` module inside each app listed in INSTALLED_APPS
# ------------------------------------------------------------------------------
app.autodiscover_tasks(settings.INSTALLED_APPS)
