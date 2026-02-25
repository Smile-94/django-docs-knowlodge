from pydantic import Field, model_validator
from pydantic_settings import BaseSettings as PydanticBaseSettings, SettingsConfigDict

from config.django.installed_apps import installed_apps_config
from config.environment import env_config


class AuthenticationSettings(PydanticBaseSettings):
    """
    Authentication settings loaded via Pydantic.
    """

    # Auth User model
    AUTH_USER_MODEL: str = Field(
        default=(
            "user.User"
            if any(app.startswith("apps.user") or app == "user" for app in installed_apps_config.INSTALLED_APPS)
            else "auth.User"
        )
    )

    TOKEN_SECRET_KEY: str = Field(default="!@#$%^&*()_+1234567890-=")
    ACCESS_TOKEN_TTL: int = Field(default=3600)
    REFRESH_TOKEN_TTL: int = Field(default=1209600)
    AUTHENTICATION_BACKENDS: list[str] = Field(
        default_factory=lambda: [
            "django.contrib.auth.backends.ModelBackend",
        ]
    )

    # Pydantic configuration
    model_config = SettingsConfigDict(
        env_file=env_config.ENVIRONMENT_FILE,  # load environment-specific .env
        extra="ignore",  # ignore unknown environment variables
    )

    # Django password validator definitions (final structure expected by Django)
    AUTH_PASSWORD_VALIDATORS: list[dict] = Field(default_factory=list)

    @model_validator(mode="after")
    def build_auth_password_validators(self) -> "AuthenticationSettings":
        # Enforce a fixed, secure set of password validators
        # to avoid partial or unsafe configuration via environment variables
        self.AUTH_PASSWORD_VALIDATORS = [
            {
                "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
            },
            {
                "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
            },
            {
                "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
            },
            {
                "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
            },
        ]
        return self


authentication_config = AuthenticationSettings()
