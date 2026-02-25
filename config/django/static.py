import os
from pathlib import PosixPath
from typing import Any

from pydantic_settings import BaseSettings

from config.django.base import base_config


class StaticSettings(BaseSettings):
    """
    Static and media file configuration for Django.
    """

    # URL prefix for static assets
    STATIC_URL: str = "/static/"

    # Filesystem location where static files are collected
    STATIC_ROOT: PosixPath = os.path.join(base_config.BASE_DIR, "static")

    # Django storage backends (Whitenoise for optimized static file serving)
    STORAGES: dict[str, dict[str, Any]] = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

    # URL prefix for user-uploaded media
    MEDIA_URL: str = "/media/"

    # Filesystem location for uploaded media files
    MEDIA_ROOT: PosixPath = os.path.join(base_config.BASE_DIR, "media")


# Singleton static/media configuration instance
static_config = StaticSettings()
