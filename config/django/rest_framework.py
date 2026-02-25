from typing import Any

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings

from config.environment import EnvironmentChoices, env_config


class RestFrameworkSettings(BaseSettings):
    """
    Django REST Framework settings.

    Design goals:
    - Security first (auth, permissions, throttling)
    - Predictable behavior across environments
    - Centralized, explicit configuration (no magic defaults)
    """

    # Final DRF settings dict consumed by Django
    REST_FRAMEWORK: dict[str, Any] = Field(default_factory=dict)

    # Global permission policy (override per-view when needed)
    # NOTE: Use IsAuthenticated in production
    DEFAULT_PERMISSION_CLASSES: list[str] = Field(
        default_factory=list,
        description="Global permission policy for DRF views",
    )

    # Supported authentication mechanisms
    # Session → browsable API
    # Basic  → legacy / internal tools
    # Token  → programmatic access
    DEFAULT_AUTHENTICATION_CLASSES: list[str] = [
        "apps.common.authentication.DeviceTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ]

    # Throttling strategy:
    # - anon   → unauthenticated users
    # - user   → authenticated users
    # - scoped → sensitive endpoints (login, OTP, writes)
    DEFAULT_THROTTLE_CLASSES: list[str] = [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",
    ]

    # Default throttle limits (override per-scope as needed)
    DEFAULT_THROTTLE_RATES: dict[str, str] = {
        "anon": "1000/hour",  # shared across all endpoints
        "user": "1000/hour",  # per authenticated user
        "scoped": "1000/hour",  # per throttle_scope
    }

    # Accepted request payload formats
    DEFAULT_PARSER_CLASSES: list[str] = [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ]

    # Response renderers
    # Browsable API is useful for internal tooling; disable in prod if needed
    DEFAULT_RENDERER_CLASSES: list[str] = ["rest_framework.renderers.JSONRenderer"]

    # Centralized exception handling for consistent error responses
    EXCEPTION_HANDLER: str = "apps.common.exception_handler.exception_handler"

    # Pagination strategy (limit/offset works best for large datasets)
    DEFAULT_PAGINATION_CLASS: str = "rest_framework.pagination.LimitOffsetPagination"

    # Default page size for list endpoints
    PAGE_SIZE: int = 10

    # Hard timeout for API views (seconds)
    DEFAULT_TIMEOUT: int = 3600

    # Default schema class for API views
    DEFAULT_SCHEMA_CLASS: str = Field(
        default="drf_spectacular.openapi.AutoSchema", description="Default schema class for API views"
    )

    # Default permission policy for DRF views
    @model_validator(mode="after")
    def set_default_permissions(self):
        if env_config.ENVIRONMENT == EnvironmentChoices.PRODUCTION.value:
            self.DEFAULT_PERMISSION_CLASSES = [
                "rest_framework.permissions.AllowAny",
                "apps.common.authentication.DeviceTokenAuthentication",
            ]
        else:
            self.DEFAULT_PERMISSION_CLASSES = [
                "rest_framework.permissions.AllowAny",
                "apps.common.authentication.DeviceTokenAuthentication",
            ]
        return self

    # # Default renderer for browsable API
    # @model_validator(mode="after")
    # def set_default_renderer(self):
    #     # Default renderer for browsable API
    #     if env_config.ENVIRONMENT != EnvironmentChoices.PRODUCTION.value:
    #         self.DEFAULT_RENDERER_CLASSES = ["rest_framework.renderers.BrowsableAPIRenderer"]
    #     return self

    @model_validator(mode="after")
    def build_rest_framework(self) -> "RestFrameworkSettings":
        """
        Assemble the final REST_FRAMEWORK dictionary.

        This ensures:
        - Single source of truth
        - No accidental divergence between fields and Django settings
        """
        self.REST_FRAMEWORK = {
            "DEFAULT_PERMISSION_CLASSES": self.DEFAULT_PERMISSION_CLASSES,
            "DEFAULT_AUTHENTICATION_CLASSES": self.DEFAULT_AUTHENTICATION_CLASSES,
            "DEFAULT_THROTTLE_CLASSES": self.DEFAULT_THROTTLE_CLASSES,
            "DEFAULT_THROTTLE_RATES": self.DEFAULT_THROTTLE_RATES,
            "DEFAULT_PARSER_CLASSES": self.DEFAULT_PARSER_CLASSES,
            "DEFAULT_RENDERER_CLASSES": self.DEFAULT_RENDERER_CLASSES,
            "EXCEPTION_HANDLER": self.EXCEPTION_HANDLER,
            "DEFAULT_PAGINATION_CLASS": self.DEFAULT_PAGINATION_CLASS,
            "PAGE_SIZE": self.PAGE_SIZE,
            "DEFAULT_TIMEOUT": self.DEFAULT_TIMEOUT,
            "DEFAULT_SCHEMA_CLASS": self.DEFAULT_SCHEMA_CLASS,
        }
        return self


# Singleton DRF configuration instance
drf_config = RestFrameworkSettings()
