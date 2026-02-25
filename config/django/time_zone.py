from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.environment import env_config


class TimeZoneSettings(BaseSettings):
    """
    Django time zone configuration assembled via Pydantic.
    """

    # Default language for the application
    LANGUAGE_CODE: str = Field(default="en-us", description="Default language for the application")

    # Default time zone for the application
    TIME_ZONE: str = Field(default="UTC", description="Default time zone for the application")

    # Enable Django’s translation system
    USE_I18N: bool = Field(default=True, description="Enable Django’s translation system")

    # Store datetimes in UTC and convert to local time when needed
    USE_TZ: bool = Field(default=True, description="Store datetimes in UTC and convert to local time when needed")

    model_config = SettingsConfigDict(
        # Load environment-specific .env file
        env_file=env_config.ENVIRONMENT_FILE,
        # Ignore unrelated environment variables
        extra="ignore",
        # Enforce exact environment variable names
        case_sensitive=True,
    )


time_zone_config = TimeZoneSettings()
