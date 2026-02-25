from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.environment import env_config


class SessionsSettings(BaseSettings):
    """
    Django session settings loaded via Pydantic.

    Features:
    - Typed and environment-aware
    - Uses cache-backed sessions (Redis recommended)
    - Secure cookie settings for HTTPS
    - Optional session lifetime and sliding expiration
    """

    # Session engine: cache backend (recommended for production)
    SESSION_ENGINE: str = Field(
        default="django.contrib.sessions.backends.cache", frozen=True, description="Django session backend engine"
    )

    # Alias of the cache backend to use (matches CACHES setting)
    SESSION_CACHE_ALIAS: str = Field(default="default", frozen=True, description="Cache alias to store sessions")

    # Only send session cookies over HTTPS
    SESSION_COOKIE_SECURE: bool = Field(default=True, frozen=True, description="Ensure session cookies are only sent over HTTPS")

    # Prevent JavaScript access to session cookies
    SESSION_COOKIE_HTTPONLY: bool = Field(
        default=True, frozen=True, description="Prevent client-side scripts from reading the cookie"
    )

    # SameSite protection against CSRF
    SESSION_COOKIE_SAMESITE: str = Field(default="Lax", frozen=True, description="Restrict cookie to same-site requests")

    # Should sessions expire when browser closes?
    SESSION_EXPIRE_AT_BROWSER_CLOSE: bool = Field(default=False, frozen=True, description="Expire session at browser close")

    # Session lifetime in seconds (default 1 day)
    SESSION_COOKIE_AGE: int = Field(default=86400, frozen=True, description="Session lifetime in seconds")

    # Update expiry on every request (sliding session)
    SESSION_SAVE_EVERY_REQUEST: bool = Field(
        default=False, frozen=True, description="Refresh session expiry time on each request"
    )

    model_config = SettingsConfigDict(
        # Load environment-specific .env file
        env_file=env_config.ENVIRONMENT_FILE,
        # Ignore unrelated environment variables
        extra="ignore",
        # Enforce exact environment variable names
        case_sensitive=True,
    )

    @field_validator("SESSION_CACHE_ALIAS", mode="before")
    @classmethod
    def validate_cache_alias(cls, value):
        # Enforce a fixed, secure set of cache aliases
        # to avoid partial or unsafe configuration via environment variables
        if value not in ["default", "redis"]:
            raise ValueError("SESSION_CACHE_ALIAS must be one of ['default', 'redis']")
        return value


sessions_config = SessionsSettings()
