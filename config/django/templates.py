from pydantic import Field, model_validator
from pydantic_settings import BaseSettings

from config.django.base import base_config


class TemplateSettings(BaseSettings):
    """
    Django template engine configuration built via Pydantic.
    """

    # Final Django-compatible TEMPLATES setting
    TEMPLATES: list[dict] = Field(default_factory=list)

    @model_validator(mode="after")
    def build_templates(self) -> "TemplateSettings":
        # Construct the DjangoTemplates backend with project-level templates
        self.TEMPLATES = [
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                # Global templates directory (in addition to app templates)
                "DIRS": [base_config.BASE_DIR / "templates"],
                # Enable template discovery inside installed apps
                "APP_DIRS": True,
                "OPTIONS": {
                    # Required context processors for auth and messaging
                    "context_processors": [
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                        "apps.common.context_processors.system_name",
                    ],
                },
            }
        ]
        return self


# Singleton template configuration instance
template_config = TemplateSettings()
