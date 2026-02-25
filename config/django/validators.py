from config.django.base import base_config
from config.environment import EnvironmentChoices, env_config


def validate_production_settings():
    # Enforce mandatory host whitelisting in production
    if env_config.ENVIRONMENT == EnvironmentChoices.PRODUCTION and not base_config.ALLOWED_HOSTS:
        raise RuntimeError("ALLOWED_HOSTS must be set in production")

    # Prevent insecure deployments with DEBUG enabled
    if base_config.DEBUG:
        raise RuntimeError("DEBUG must be False in production")
