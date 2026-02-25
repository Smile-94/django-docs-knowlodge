from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.environment import env_config


class SecuritySettings(BaseSettings):
    """
    Security-critical Django settings loaded via Pydantic.
    """

    # Enables Django debug features (must be False in production)
    DEBUG: bool = Field(
        default=False,
        description="Whether the application is running in debug mode",
    )

    # Cryptographic secret used by Django (must be provided via environment)
    SECRET_KEY: SecretStr = Field(..., frozen=True, description="Django secret key")

    BROKER_API_ENCRYPTION_KEY: str = Field(..., frozen=True, description="Broker API encryption key")

    @field_validator("SECRET_KEY", mode="before")
    @classmethod
    def validate_secret_key(cls, value):
        # Fail fast if SECRET_KEY is missing to prevent insecure startup
        if not value:
            raise ValueError("SECRET_KEY must be set")
        return value

    @field_validator("BROKER_API_ENCRYPTION_KEY", mode="before")
    @classmethod
    def validate_broker_api_encryption_key(cls, value):
        # Fail fast if BROKER_API_ENCRYPTION_KEY is missing to prevent insecure startup
        if not value:
            raise ValueError("BROKER_API_ENCRYPTION_KEY must be set")
        return value

    model_config = SettingsConfigDict(
        # Load environment-specific .env file
        env_file=env_config.ENVIRONMENT_FILE,
        # Ignore unrelated environment variables
        extra="ignore",
        # Enforce exact environment variable names
        case_sensitive=True,
    )


# Singleton security configuration instance
security_config = SecuritySettings()
