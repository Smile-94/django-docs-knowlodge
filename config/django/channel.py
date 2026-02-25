from typing import Any
from pydantic import Field
from pydantic_settings import BaseSettings
from config.django.cache import cache_config


class ChannelSettings(BaseSettings):
    """
    This class defines the setting configuration for the channel layer.
    """

    CHANNEL_LAYERS: dict[str, Any] = Field(
        default={
            "default": {
                "BACKEND": "channels_redis.core.RedisChannelLayer",
                "CONFIG": {
                    "hosts": [(cache_config.REDIS_HOST, cache_config.REDIS_PORT)],
                },
            },
        },
        frozen=True,
    )


channel_config = ChannelSettings()
