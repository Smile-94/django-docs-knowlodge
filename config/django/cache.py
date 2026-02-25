from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.environment import env_config


class CacheSettings(BaseSettings):
    """
    Redis configuration loaded via Pydantic.

    considerations:
    - Uses django-redis backend for caching to ensure high performance.
    - Passwords are stored as SecretStr and hidden from repr/logs for security.
    - Supports environment-specific .env files for multi-environment deployments.
    - Provides validation and default fallbacks for safe defaults.
    - Singleton pattern ensures consistent configuration throughout the project.
    """

    # Redis hostname/IP address, hidden from logs to avoid accidental leaks
    REDIS_HOST: str = Field(default="localhost", frozen=True, repr=False)

    # Redis port number, standard default 6379
    REDIS_PORT: int = Field(default=6379, frozen=True, repr=False)

    # Redis database index; validate >= 0
    REDIS_DB: int = Field(default=1, frozen=True, repr=False)

    # Dedicated Redis DB for Celery broker (avoid collision with Django cache)
    REDIS_DB_BROKER: int = Field(default=2, frozen=True, repr=False)

    # Dedicated Redis DB for Celery result backend
    REDIS_DB_BACKEND: int = Field(default=3, frozen=True, repr=False)

    # Redis password, wrapped in SecretStr for security, hidden from logs
    REDIS_PASSWORD: SecretStr = Field(default=SecretStr(""), frozen=True, repr=False)

    # Cache timeout in seconds, hidden from logs to avoid accidental leaks
    CACHES_TIMEOUT: int = Field(default=60, frozen=True, repr=False)

    # Socket connect timeout in seconds, hidden from logs to avoid accidental leaks
    SOCKET_CONNECT_TIMEOUT: int = Field(default=60, frozen=True, repr=False)

    # Socket timeout in seconds, hidden from logs to avoid accidental leaks
    SOCKET_TIMEOUT: int = Field(default=60, frozen=True, repr=False)

    # Ignore exceptions, hidden from logs to avoid accidental leaks
    IGNORE_EXCEPTIONS: bool = Field(default=False, frozen=True, repr=False)

    # Retry on timeout, hidden from logs to avoid accidental leaks
    RETRY_ON_TIMEOUT: bool = Field(default=False, frozen=True, repr=False)

    # Final Django CACHES dictionary
    CACHES: dict = Field(default_factory=dict)

    # Pydantic configuration
    model_config = SettingsConfigDict(
        env_file=env_config.ENVIRONMENT_FILE,  # load environment-specific .env
        extra="ignore",  # ignore unknown environment variables
    )

    @field_validator("REDIS_DB")
    def validate_db(cls, v: int) -> int:
        # Ensure Redis DB index is non-negative
        if v < 0:
            raise ValueError("REDIS_DB must be >= 0")
        return v

    @model_validator(mode="after")
    def build_redis_config(self) -> "CacheSettings":
        """
        Build Django CACHES configuration.

        Features:
        - Uses redis:// scheme for simplicity; can be extended to rediss:// for SSL.
        - Adds password only if provided; avoids sending empty password.
        - Uses django_redis.client.DefaultClient for robust connection handling.
        - Can be extended with SOCKET_TIMEOUT, IGNORE_EXCEPTIONS, etc. for production.
        """
        self.CACHES = {
            "default": {
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}",
                "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
                "TIMEOUT": self.CACHES_TIMEOUT,
            }
        }

        if self.REDIS_PASSWORD and self.REDIS_PASSWORD.get_secret_value():
            self.CACHES["default"]["OPTIONS"]["PASSWORD"] = self.REDIS_PASSWORD.get_secret_value()

        # Enable socket connect timeout for production
        if self.SOCKET_CONNECT_TIMEOUT:
            self.CACHES["default"]["OPTIONS"]["SOCKET_CONNECT_TIMEOUT"] = self.SOCKET_CONNECT_TIMEOUT

        # Enable socket timeout for production
        if self.SOCKET_TIMEOUT:
            self.CACHES["default"]["OPTIONS"]["SOCKET_TIMEOUT"] = self.SOCKET_TIMEOUT

        # Enable exceptions to be ignored for production
        if self.IGNORE_EXCEPTIONS:
            self.CACHES["default"]["OPTIONS"]["IGNORE_EXCEPTIONS"] = (
                self.IGNORE_EXCEPTIONS
            )  # Crucial for Production: If Redis is down, Django won't 500

        # Enable retry on timeout for production
        if self.RETRY_ON_TIMEOUT:
            self.CACHES["default"]["OPTIONS"]["RETRY_ON_TIMEOUT"] = self.RETRY_ON_TIMEOUT

        return self


# Singleton cache configuration instance
cache_config = CacheSettings()
