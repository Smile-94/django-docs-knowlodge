# settings/asgi.py

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from apps.broker.routing import websocket_urlpatterns as broker_ws_urlpatterns
from apps.order.routing import websocket_urlpatterns as order_ws_urlpatterns

# import apps.orders.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(order_ws_urlpatterns + broker_ws_urlpatterns)),
    }
)
