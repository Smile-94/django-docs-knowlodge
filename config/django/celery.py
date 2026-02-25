from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.django.cache import cache_config
from config.environment import env_config


class CelerySettings(BaseSettings):
    # Restrict accepted content types to JSON only (security + consistency)
    CELERY_ACCEPT_CONTENT: list[str] = Field(default=["json"], frozen=True)

    # Use JSON to avoid pickle RCE vulnerabilities
    CELERY_TASK_SERIALIZER: str = Field(default="json", frozen=True)
    CELERY_RESULT_SERIALIZER: str = Field(default="json", frozen=True)

    # ----------------------------
    # Time & timezone
    # ----------------------------

    # Force UTC to avoid DST-related bugs across workers
    CELERY_ENABLE_UTC: bool = Field(default=True, frozen=True)

    # Explicit timezone declaration (important for scheduled tasks)
    CELERY_TIMEZONE: str = Field(default="UTC", frozen=True)

    # ----------------------------
    # Reliability & delivery guarantees
    # ----------------------------

    # Acknowledge tasks *after* execution to prevent task loss on worker crash
    CELERY_TASK_ACKS_LATE: bool = Field(default=True, frozen=True)

    # Re-queue task if worker crashes mid-execution
    CELERY_TASK_REJECT_ON_WORKER_LOST: bool = Field(default=True, frozen=True)

    # Ensure Celery retries broker connection during startup (Docker-safe)
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP: bool = Field(default=True, frozen=True)

    # Prevent worker from prefetching multiple tasks (important for long jobs)
    CELERY_WORKER_PREFETCH_MULTIPLIER: int = Field(default=1, frozen=True)

    # ----------------------------
    # Computed Django-compatible values
    # ----------------------------

    # Fully-built Redis URL for Celery broker
    CELERY_BROKER_URL: str | None = None

    # Fully-built Redis URL for result backend
    CELERY_RESULT_BACKEND: str | None = None

    # ----------------------------
    # Pydantic configuration
    # ----------------------------

    model_config = SettingsConfigDict(
        env_file=env_config.ENVIRONMENT_FILE,  # environment-specific .env loading
        extra="ignore",  # ignore unrelated env vars safely
    )

    @model_validator(mode="after")
    def build_celery_urls(self) -> "CelerySettings":
        # Inject password only when explicitly provided
        # Avoids malformed redis:// URLs with empty credentials
        password = ""
        if cache_config.REDIS_PASSWORD and cache_config.REDIS_PASSWORD.get_secret_value():
            password = f":{cache_config.REDIS_PASSWORD.get_secret_value()}@"

        # Broker handles task queueing and delivery
        self.CELERY_BROKER_URL = (
            f"redis://{password}{cache_config.REDIS_HOST}:{cache_config.REDIS_PORT}/{cache_config.REDIS_DB_BROKER}"
        )

        # Backend stores task results and states
        self.CELERY_RESULT_BACKEND = (
            f"redis://{password}{cache_config.REDIS_HOST}:{cache_config.REDIS_PORT}/{cache_config.REDIS_DB_BACKEND}"
        )

        return self


# Singleton instance ensures one immutable config across Django & Celery
celery_config = CelerySettings()
