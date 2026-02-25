import logging

from django.db import connection
from django.test import RequestFactory
import redis
from rest_framework.views import APIView

from _library.error_codes import INTERNAL_SERVER_ERROR
from _library.functions.allowed_method import allowed_methods
from _library.functions.formatters import response_formatter
from _library.success_code import SUCCESS_RESPONSE_200
from apps.broker.views.signals_parse_view import ReceiveSignalAPIView
from apps.common.documentation import SystemDocumentation
from config.celery import app
from config.django.cache import cache_config

logger = logging.getLogger(__name__)


# <<--------------------------------- System Health Check View --------------------------------->>
@allowed_methods("GET")
class SystemHealthCheckAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @SystemDocumentation.health_check()
    def get(self, request):
        try:
            data = {
                "database": self.check_database(),
                "redis": self.check_redis(),
                "celery": self.check_celery(),
                "webhook": self.check_webhook(),
            }

            data["status"] = "healthy" if all(data.values()) else "unhealthy"
            data["message"] = f"System are {data['status']}"

            return response_formatter(SUCCESS_RESPONSE_200, data)
        except Exception as e:
            logger.exception(f"ERROR:---------->>System Health Check View error: {e}")
            return response_formatter(INTERNAL_SERVER_ERROR)

    def check_database(self) -> bool:
        try:
            connection.ensure_connection()
            return True
        except Exception:
            return False

    def check_redis(self) -> bool:
        try:
            r = redis.Redis(host=cache_config.REDIS_HOST, port=cache_config.REDIS_PORT, socket_connect_timeout=2)
            r.ping()
            return True
        except Exception as e:
            logger.exception(f"ERROR:---------->>System Health redis error: {e}")
            return False

    def check_celery(self):
        insp = app.control.inspect()
        if insp.ping():
            return True
        return False

    def check_webhook(self):
        """
        Simulate a fake webhook request to test API logic.
        """
        try:
            factory = RequestFactory()

            fake_request = factory.post(
                "/api/v1/broker/webhook/", data="HEALTH_CHECK_TEST", content_type="text/plain", HTTP_X_API_KEY="ajsdfjsdjahfk"
            )

            # Call webhook view directly
            ReceiveSignalAPIView.as_view()(fake_request)

            return True

        except Exception:
            return False
