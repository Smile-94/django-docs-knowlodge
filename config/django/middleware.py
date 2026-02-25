from pydantic import model_validator
from pydantic_settings import BaseSettings

from config.environment import env_config


class MiddlewareSettings(BaseSettings):
    """
    Django middleware configuration assembled via Pydantic.
    """

    # Core Django middleware (order-sensitive)
    MIDDLEWARE: list[str] = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    # Third-party middleware shared across environments
    THIRD_PARTY_MIDDLEWARE: list[str] = [
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

    # Project-specific custom middleware
    CUSTOM_MIDDLEWARE: list[str] = [
        "apps.common.middleware.custom_middleware.CacheRequestBodyMiddleware",
        "apps.common.middleware.custom_middleware.RequestLoggingMiddleware",
        "apps.common.middleware.custom_middleware.RequestTimingMiddleware",
        "apps.common.middleware.custom_middleware.AddCspNonceMiddleware",
        "apps.common.middleware.custom_middleware.UrlValidationMiddleware",
    ]

    @model_validator(mode="after")
    def set_middleware(self):
        # Append third-party middleware after core middleware
        if self.THIRD_PARTY_MIDDLEWARE:
            self.MIDDLEWARE += self.THIRD_PARTY_MIDDLEWARE

        # Append custom middleware last to preserve override behavior
        if self.CUSTOM_MIDDLEWARE:
            self.MIDDLEWARE += self.CUSTOM_MIDDLEWARE

        return self


# Singleton middleware configuration instance
middleware_config = MiddlewareSettings()
