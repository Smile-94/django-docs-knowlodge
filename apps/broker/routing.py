# apps/broker/routing.py

from django.urls import path

from apps.broker.consumers.consumers import SignalInvalidConsumer

websocket_urlpatterns = [
    path("ws/signals/invalid/", SignalInvalidConsumer.as_asgi()),
]
