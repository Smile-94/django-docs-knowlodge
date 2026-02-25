from django.urls import path

from apps.common.views import SystemHealthCheckAPIView

urlpatterns = [
    path("health/", SystemHealthCheckAPIView.as_view()),
]
