from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from apps.broker import urls as broker_urls
from apps.common import urls as common_urls
from apps.order import urls as order_urls
from apps.user import urls as user_urls
from config.django.security import security_config

urlpatterns = [
    path("admin/", admin.site.urls),
]

urlpatterns += [
    path("api/v1/user/", include(user_urls)),
    path("api/v1/broker/", include(broker_urls)),
    path("api/v1/order/", include(order_urls)),
    path("api/v1/", include(common_urls)),
]

if security_config.DEBUG:
    urlpatterns += [
        path("dev/api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path("dev/api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
        path("dev/api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    ] + debug_toolbar_urls()
