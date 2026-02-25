from enum import Enum

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentChoices(str, Enum):
    # Supported runtime environments
    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class EnvironmentSettings(BaseSettings):
    # Active runtime environment (immutable after load)
    ENVIRONMENT: EnvironmentChoices = Field(
        default=EnvironmentChoices.LOCAL,
        frozen=True,
        description="Current runtime environment",
    )

    @computed_field
    def ENVIRONMENT_FILE(self) -> str:
        # Derive environment-specific .env file from ENVIRONMENT
        # Example: env/.env.production
        return f"_environment/.env.{self.ENVIRONMENT.value}"

    model_config = SettingsConfigDict(
        # Base .env file used only to resolve ENVIRONMENT
        env_file="_environment/.env",
        # Ignore unrelated environment variables
        extra="ignore",
    )


# Singleton environment configuration instance
env_config = EnvironmentSettings()
