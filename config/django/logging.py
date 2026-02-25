from pydantic import Field, model_validator
from pydantic_settings import BaseSettings


class LoggingSettings(BaseSettings):
    """
    Django logging settings.
    """

    LOGGING: dict = Field(default_factory=dict, description="Django logging configuration")
    # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    FORMATTERS: dict = {
        "verbose": {
            "format": "{levelname} {asctime} [{module}:{lineno}] {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }

    # Logging handlers (console, file, email)
    HANDLERS: dict = {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "level": "DEBUG",
        },
        # "file": {
        #     "class": "logging.FileHandler",
        #     "formatter": "verbose",
        #     "level": "DEBUG",
        #     "filename": "django.log",
        # },
        # "email": {
        #     "class": "logging.handlers.SMTPHandler",
        #     "formatter": "verbose",
        #     "level": "ERROR",
        #     "mailhost": "localhost",
        #     "fromaddr": "django@example.com",
        #     "toaddrs": "admin@example.com",
        #     "subject": "Django Error",
        # },  # TODO: Add email settings
    }

    ROOT: dict = {
        "handlers": ["console"],
        "level": "DEBUG",
    }

    LOGGERS: dict = {
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.utils.autoreload": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    }

    @model_validator(mode="after")
    def build_logging(self) -> "LoggingSettings":
        """
        Build Django logging configuration.
        """
        self.LOGGING = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": self.FORMATTERS,
            "handlers": self.HANDLERS,
            "root": self.ROOT,
            "loggers": self.LOGGERS,
        }
        return self


logging_config = LoggingSettings()
