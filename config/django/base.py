import ipaddress
from pathlib import Path, PosixPath

from pydantic import AliasChoices, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.environment import env_config


class BaseSettings(BaseSettings):
    """
    Core Django settings loaded via Pydantic.
    Acts as the foundation for all environment-specific settings.
    """

    # Absolute project root directory (immutable after initialization)
    BASE_DIR: PosixPath = Field(
        default=Path(__file__).resolve().parent.parent.parent,
        frozen=True,
    )

    # Django runtime host configuration
    ALLOWED_HOSTS: list[str] = []
    INTERNAL_IPS: list[str] = []

    # Comma-separated host/IP source loaded from environment
    SERVER_NAME: str = Field(
        default="",
        validation_alias=AliasChoices("SERVER_NAME"),
    )

    # Django application entry points
    ASGI_APPLICATION: str = "config.asgi.application"
    ROOT_URLCONF: str = "routes.urls"

    DEBUG_TOOLBAR_CONFIG: dict = {"SHOW_TOOLBAR_CALLBACK": lambda request: not request.path.startswith("/api/")}

    @model_validator(mode="after")
    def parse_allowed_hosts(self) -> "BaseSettings":
        # Derive ALLOWED_HOSTS from SERVER_NAME to ensure
        # a single source of truth for host configuration
        if self.SERVER_NAME:
            self.ALLOWED_HOSTS = [host.strip() for host in self.SERVER_NAME.split(",") if host.strip()]
        return self

    @model_validator(mode="after")
    def parse_internal_ips(self) -> "BaseSettings":
        # INTERNAL_IPS is restricted to valid IP addresses only
        # (used by Django debug tools and internal access checks)
        if not self.SERVER_NAME:
            self.INTERNAL_IPS = []
            return self

        self.INTERNAL_IPS = [
            cleaned
            for cleaned in (item.strip() for item in self.SERVER_NAME.split(","))
            if cleaned and self._is_valid_ip(cleaned)
        ]
        return self

    @staticmethod
    def _is_valid_ip(value: str) -> bool:
        # Validate IPv4 / IPv6 addresses safely
        try:
            ipaddress.ip_address(value)
            return True
        except ValueError:
            return False

    model_config = SettingsConfigDict(
        # Environment-specific .env file selected by env_config
        env_file=env_config.ENVIRONMENT_FILE,
        # Ignore unknown environment variables to allow shared infra envs
        extra="ignore",
    )


# Singleton base configuration instance used across Django settings
base_config = BaseSettings()
