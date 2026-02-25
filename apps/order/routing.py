# apps/orders/routing.py

from django.urls import path

from apps.order.consumer.consumers import OrderConsumer

websocket_urlpatterns = [
    path("ws/orders/", OrderConsumer.as_asgi()),
]
