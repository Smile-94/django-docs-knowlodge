from pydantic import model_validator
from pydantic_settings import BaseSettings

from config.environment import env_config


class InstalledAppsSettings(BaseSettings):
    """
    Django INSTALLED_APPS configuration assembled via Pydantic.
    """

    # Core Django framework applications (always enabled)
    DJANGO_APPS: list[str] = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]

    # Third-party applications common across environments
    THIRD_PARTY_APPS: list[str] = [
        "channels",
        "rangefilter",
        "django_filters",
        "rest_framework",
        "drf_spectacular",
        "drf_spectacular_sidecar",
        "debug_toolbar",
    ]

    # Project-specific Django apps
    LOCAL_APPS: list[str] = [
        "apps.common.apps.CommonConfig",
        "apps.user.apps.UserConfig",
        "apps.broker.apps.BrokerConfig",
        "apps.order.apps.OrderConfig",
    ]

    # Final Django-compatible INSTALLED_APPS list
    INSTALLED_APPS: list[str] = []

    @model_validator(mode="after")
    def set_apps(self):
        # Preserve Django app loading order: core → third-party → local
        self.INSTALLED_APPS = list(self.DJANGO_APPS + self.THIRD_PARTY_APPS + self.LOCAL_APPS)
        return self


# Singleton instance used by Django settings
installed_apps_config = InstalledAppsSettings()
