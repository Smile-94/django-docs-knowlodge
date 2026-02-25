# ------------------------------------------------------------------------------
# Import modular Django configuration sections
# Each config is isolated to keep settings clean, testable, and environment-safe
# ------------------------------------------------------------------------------
from config.django.authentication import authentication_config
from config.django.base import base_config
from config.django.cache import cache_config
from config.django.celery import celery_config
from config.django.database import database_config
from config.django.documentation import documentation_config
from config.django.installed_apps import installed_apps_config
from config.django.logging import logging_config
from config.django.middleware import middleware_config
from config.django.rest_framework import drf_config
from config.django.security import security_config
from config.django.sessions import sessions_config
from config.django.static import static_config
from config.django.templates import template_config
from config.django.time_zone import time_zone_config
from config.django.channel import channel_config

# ------------------------------------------------------------------------------
# Core project paths and base configuration
# ------------------------------------------------------------------------------
# Absolute base directory of the Django project (used across settings)
BASE_DIR = base_config.BASE_DIR


# ------------------------------------------------------------------------------
# Security settings
# ------------------------------------------------------------------------------
# Secret key used for cryptographic signing (must be unique per environment)
SECRET_KEY = security_config.SECRET_KEY

# Debug should ALWAYS be False in production
DEBUG = security_config.DEBUG

# Broker API encryption key
BROKER_API_ENCRYPTION_KEY = security_config.BROKER_API_ENCRYPTION_KEY

# Hosts/domain names that this Django site can serve
# Prevents HTTP Host header attacks
ALLOWED_HOSTS = base_config.ALLOWED_HOSTS


# ------------------------------------------------------------------------------
# Application definition
# ------------------------------------------------------------------------------
# All installed Django, third-party, and local apps
INSTALLED_APPS = installed_apps_config.INSTALLED_APPS

# Middleware stack executed on every request/response cycle
# Order matters — security middleware should come first
MIDDLEWARE = middleware_config.MIDDLEWARE


# ------------------------------------------------------------------------------
# URL and application entry points
# ------------------------------------------------------------------------------
# Root URL configuration module
ROOT_URLCONF = base_config.ROOT_URLCONF

# ASGI entry point (used for async support, WebSockets, and background tasks)
# WSGI_APPLICATION = base_config.ASGI_APPLICATION

# WSGI for runserver / uwsgi / gunicorn wsgi
# WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = base_config.ASGI_APPLICATION

# ------------------------------------------------------------------------------
# Templates configuration
# ------------------------------------------------------------------------------
# Django template engine configuration
# Includes template loaders, context processors, and directories
TEMPLATES = template_config.TEMPLATES


# ------------------------------------------------------------------------------
# Database configuration
# ------------------------------------------------------------------------------
# Database connections (PostgreSQL / MySQL / SQLite etc.)
# Loaded dynamically per environment
DATABASES = database_config.DATABASES


# ------------------------------------------------------------------------------
# Authentication and password validation
# ------------------------------------------------------------------------------
# Auth User model
AUTH_USER_MODEL = authentication_config.AUTH_USER_MODEL

# Auth Token secret
TOKEN_SECRET_KEY = authentication_config.TOKEN_SECRET_KEY

# Auth Token expiration
ACCESS_TOKEN_TTL = authentication_config.ACCESS_TOKEN_TTL

REFRESH_TOKEN_TTL = authentication_config.REFRESH_TOKEN_TTL

# Auth Backends
AUTHENTICATION_BACKENDS = authentication_config.AUTHENTICATION_BACKENDS

# Password validators enforce strong passwords and security best practices
AUTH_PASSWORD_VALIDATORS = authentication_config.AUTH_PASSWORD_VALIDATORS


# ------------------------------------------------------------------------------
# Internationalization
# ------------------------------------------------------------------------------
# Default language for the application
LANGUAGE_CODE = time_zone_config.LANGUAGE_CODE

# Application time zone (UTC recommended for production systems)
TIME_ZONE = time_zone_config.TIME_ZONE

# Enable Django’s translation system
USE_I18N = time_zone_config.USE_I18N

# Store datetimes in UTC and convert to local time when needed
USE_TZ = time_zone_config.USE_TZ


# ------------------------------------------------------------------------------
# Static and media files
# ------------------------------------------------------------------------------
# URL prefix for static files (CSS, JS, images)
STATIC_URL = static_config.STATIC_URL

# Directory where static files are collected for production
STATIC_ROOT = static_config.STATIC_ROOT

# Storage backends (local, S3, CDN, etc.)
STORAGES = static_config.STORAGES

# URL prefix for user-uploaded media files
MEDIA_URL = static_config.MEDIA_URL

# Filesystem path for uploaded media
MEDIA_ROOT = static_config.MEDIA_ROOT


# ------------------------------------------------------------------------------
# REST Framework configuration
# ------------------------------------------------------------------------------
# DRF settings loaded via Pydantic
REST_FRAMEWORK = drf_config.REST_FRAMEWORK

# ------------------------------------------------------------------------------
# Cache configuration
# ------------------------------------------------------------------------------
CACHES = cache_config.CACHES


# ------------------------------------------------------------------------------
# Sessions configuration
# ------------------------------------------------------------------------------
SESSION_ENGINE = sessions_config.SESSION_ENGINE
SESSION_CACHE_ALIAS = sessions_config.SESSION_CACHE_ALIAS
SESSION_COOKIE_SECURE = sessions_config.SESSION_COOKIE_SECURE
SESSION_COOKIE_HTTPONLY = sessions_config.SESSION_COOKIE_HTTPONLY
SESSION_COOKIE_SAMESITE = sessions_config.SESSION_COOKIE_SAMESITE
SESSION_EXPIRE_AT_BROWSER_CLOSE = sessions_config.SESSION_EXPIRE_AT_BROWSER_CLOSE
SESSION_COOKIE_AGE = sessions_config.SESSION_COOKIE_AGE
SESSION_SAVE_EVERY_REQUEST = sessions_config.SESSION_SAVE_EVERY_REQUEST

# ------------------------------------------------------------------------------
# Documentation configuration
# ------------------------------------------------------------------------------
SPECTACULAR_SETTINGS = documentation_config.SPECTACULAR_SETTINGS

# ------------------------------------------------------------------------------
# Logging configuration
# ------------------------------------------------------------------------------
LOGGING = logging_config.LOGGING

# ------------------------------------------------------------------------------
# Debug toolbar configuration
# ------------------------------------------------------------------------------
INTERNAL_IPS = base_config.INTERNAL_IPS
DEBUG_TOOLBAR_CONFIG = base_config.DEBUG_TOOLBAR_CONFIG

# ------------------------------------------------------------------------------
# Celery configuration
# ------------------------------------------------------------------------------
CELERY_BROKER_URL = celery_config.CELERY_BROKER_URL
CELERY_RESULT_BACKEND = celery_config.CELERY_RESULT_BACKEND

CELERY_ACCEPT_CONTENT = celery_config.CELERY_ACCEPT_CONTENT
CELERY_TASK_SERIALIZER = celery_config.CELERY_TASK_SERIALIZER
CELERY_RESULT_SERIALIZER = celery_config.CELERY_RESULT_SERIALIZER
CELERY_ENABLE_UTC = celery_config.CELERY_ENABLE_UTC
CELERY_TIMEZONE = celery_config.CELERY_TIMEZONE

CELERY_TASK_ACKS_LATE = celery_config.CELERY_TASK_ACKS_LATE
CELERY_TASK_REJECT_ON_WORKER_LOST = celery_config.CELERY_TASK_REJECT_ON_WORKER_LOST
CELERY_WORKER_PREFETCH_MULTIPLIER = celery_config.CELERY_WORKER_PREFETCH_MULTIPLIER
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = celery_config.CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP

# ----------------------------------------------------------------------------------------------------
# CHANNELS (WEBSOCKETS)
# ----------------------------------------------------------------------------------------------------
CHANNEL_LAYERS = channel_config.CHANNEL_LAYERS
