from typing import Any

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.environment import env_config


class DocumentationSettings(BaseSettings):
    """
    Pydantic-based configuration for Django API documentation.

    considerations:
    1. Centralized, typed configuration ensures consistency across environments.
    2. Supports Swagger and ReDoc UI with customizable options.
    3. Schema path prefix and server URLs are environment-aware.
    4. Whitelists servers to avoid exposing internal APIs in production.
    """

    # ---------------------------
    # Basic API Info
    # ---------------------------
    TITLE: str = Field(default="Django Starter API", description="API title")
    DESCRIPTION: str = Field(default="Django Starter API documentation", description="API description")
    VERSION: str = Field(default="1.0.0", description="API version")
    TERMS_OF_SERVICE: str = Field(default="https://example.com/terms/", description="Terms of service URL")

    # ---------------------------
    # Contact Info
    # ---------------------------
    CONTACT_NAME: str = Field(default="Md. Sazzad Hossen", description="Contact name")
    CONTACT_URL: str = Field(default="https://example.com/support", description="Contact URL")
    CONTACT_EMAIL: str = Field(default="mshossen75@gmail.com", description="Contact email")

    # ---------------------------
    # License Info
    # ---------------------------
    LICENSE_NAME: str = Field(default="MIT", description="License name")
    LICENSE_URL: str = Field(default="https://opensource.org/licenses/MIT", description="License URL")

    # ---------------------------
    # Swagger / ReDoc options
    # ---------------------------
    SWAGGER_UI_DIST: str = Field(default="SIDECAR", description="Swagger UI distribution")
    SWAGGER_UI_FAVICON_HREF: str = Field(default="SIDECAR", description="Swagger UI favicon")
    REDOC_DIST: str = Field(default="SIDECAR", description="ReDoc UI distribution")

    # ---------------------------
    # API Path Prefix
    # ---------------------------
    SCHEMA_PATH_PREFIX: str = Field(default="/api/v1", description="Schema path prefix")
    SCHEMA_PATH_PREFIX_INSERT: str = Field(default="/api/v1", description="Schema path prefix insert")
    SCHEMA_PATH_PREFIX_TRIM: str = Field(default="/api", description="Schema prefix trim")

    # ---------------------------
    # Servers / Environments
    # ---------------------------
    SERVERS: list[dict[str, str]] = Field(
        default_factory=list,
        description="Server URLs displayed in docs",
        example=[{"url": "https://api.example.com", "description": "Production server"}],
    )

    # ---------------------------
    # Security schemes
    # ---------------------------
    SECURITY_SCHEMES: dict[str, Any] = Field(
        default_factory=dict, description="Security schemes for API (e.g., bearer token, OAuth2)"
    )
    # drf-spectacular settings container
    SPECTACULAR_SETTINGS: dict[str, Any] = Field(
        default_factory=dict,
        description="Spectacular settings for the documentation",
    )

    model_config = SettingsConfigDict(
        # Load environment-specific .env file (local, staging, production)
        env_file=env_config.ENVIRONMENT_FILE,
        # Ignore unrelated environment variables to prevent runtime errors
        extra="ignore",
        # Enforce exact environment variable names (case-sensitive)
        case_sensitive=True,
    )

    @model_validator(mode="after")
    def build_spectacular_settings(self) -> "DocumentationSettings":
        """
        Assemble drf-spectacular settings with:
        - API info
        - Contact and license info
        - Servers
        - Security schemes
        """
        self.SPECTACULAR_SETTINGS = {
            "TITLE": self.TITLE,
            "DESCRIPTION": self.DESCRIPTION,
            "VERSION": self.VERSION,
            "TERMS_OF_SERVICE": self.TERMS_OF_SERVICE,
            "CONTACT": {
                "name": self.CONTACT_NAME,
                "url": self.CONTACT_URL,
                "email": self.CONTACT_EMAIL,
            },
            "LICENSE": {
                "name": self.LICENSE_NAME,
                "url": self.LICENSE_URL,
            },
            "SWAGGER_UI_DIST": self.SWAGGER_UI_DIST,
            "SWAGGER_UI_FAVICON_HREF": self.SWAGGER_UI_FAVICON_HREF,
            "REDOC_DIST": self.REDOC_DIST,
            "SCHEMA_PATH_PREFIX": self.SCHEMA_PATH_PREFIX,
            "SCHEMA_PATH_PREFIX_INSERT": self.SCHEMA_PATH_PREFIX_INSERT,
            "SCHEMA_PATH_PREFIX_TRIM": self.SCHEMA_PATH_PREFIX_TRIM,
            "SERVERS": self.SERVERS,
            "SECURITY_SCHEMES": self.SECURITY_SCHEMES,
        }

        return self


# Singleton instance for project-wide use
documentation_config = DocumentationSettings()
