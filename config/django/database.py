from enum import Enum

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.django.base import base_config
from config.environment import env_config


class DatabaseChoices(str, Enum):
    # Supported database engines (values map to Django backends)
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    ORACLE = "oracle"
    MSSQL = "mssql"


# Maps database choice to the corresponding Django ENGINE path
ENGINE_MAP = {
    DatabaseChoices.SQLITE: "django.db.backends.sqlite3",
    DatabaseChoices.POSTGRESQL: "django.db.backends.postgresql",
    DatabaseChoices.MYSQL: "django.db.backends.mysql",
    DatabaseChoices.ORACLE: "django.db.backends.oracle",
    DatabaseChoices.MSSQL: "django.db.backends.mssql",
}


class DatabaseSettings(BaseSettings):
    """
    Database configuration built via Pydantic and exposed
    in Django's expected DATABASES structure.
    """

    # Default primary key field type for Django models
    DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"

    # Database engine selection (immutable after load)
    DATABASE_TYPE: DatabaseChoices = Field(
        default=DatabaseChoices.SQLITE,
        frozen=True,
    )

    # Connection parameters (hidden from repr/logs for safety)
    DATABASE_HOST: str = Field(default="localhost", frozen=True, repr=False)
    DATABASE_PORT: int = Field(default=5432, frozen=True, repr=False)
    DATABASE_NAME: str = Field(default="postgres", frozen=True, repr=False)
    DATABASE_USER: str = Field(default="postgres", frozen=True, repr=False)
    DATABASE_PASSWORD: SecretStr = Field(
        default="postgres",
        frozen=True,
        repr=False,
    )

    # Final Django-compatible DATABASES dict
    DATABASES: dict = Field(default_factory=dict)

    model_config = SettingsConfigDict(
        # Load environment-specific .env file
        env_file=env_config.ENVIRONMENT_FILE,
        # Ignore unrelated env vars (safe for shared infra)
        extra="ignore",
        # Enforce exact env var naming
        case_sensitive=True,
    )

    @model_validator(mode="after")
    def build_database_config(self) -> "DatabaseSettings":
        # Resolve Django backend engine from selected database type
        engine = ENGINE_MAP[self.DATABASE_TYPE]

        # SQLite uses a local file path instead of network credentials
        if self.DATABASE_TYPE == DatabaseChoices.SQLITE:
            self.DATABASES = {
                "default": {
                    "ENGINE": engine,
                    "NAME": base_config.BASE_DIR / "db.sqlite3",
                }
            }
            return self

        # Network-based databases (PostgreSQL, MySQL, etc.)
        self.DATABASES = {
            "default": {
                "ENGINE": engine,
                "NAME": self.DATABASE_NAME,
                "USER": self.DATABASE_USER,
                "PASSWORD": self.DATABASE_PASSWORD.get_secret_value(),
                "HOST": self.DATABASE_HOST,
                "PORT": self.DATABASE_PORT,
            }
        }

        return self


# Singleton database configuration instance
database_config = DatabaseSettings()
