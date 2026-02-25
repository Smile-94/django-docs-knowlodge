import logging

from rest_framework.views import APIView

from _library.error_codes import BAD_REQUEST_DEVELOPER_ERROR, BAD_REQUEST_USER_ERROR, INTERNAL_SERVER_ERROR
from _library.functions.allowed_method import allowed_methods
from _library.functions.formatters import response_formatter
from _library.success_code import SUCCESS_RESPONSE_200
from apps.broker.documentation.signal_parse_documentation import SignalDocumentation
from apps.broker.models.broker_account_model import BrokerAccount
from apps.broker.models.signals_model import TradingSignal
from apps.broker.serializers.signals_parse_serializer import SignalsParseSerializer
from apps.broker.tasks.paser_signal_task import process_signal_task
from apps.common.parser.plain_text_parser import PlainTextParser
from apps.common.security.encryption import hash_api_key

logger = logging.getLogger(__name__)


# <<--------------------------------- Receive Signal API View --------------------------------->>


@allowed_methods("POST")
class ReceiveSignalAPIView(APIView):
    authentication_classes = []
    permission_classes = []
    parser_classes = [PlainTextParser]

    model_class = BrokerAccount
    trading_signal_model = TradingSignal
    serializer_class = SignalsParseSerializer

    @SignalDocumentation.receive()
    def post(self, request):
        try:
            # Reject if X-API-KEY header is missing
            if not request.headers.get("X-API-KEY"):
                data = {"message": "No X-API-KEY header provided", "error": "X-API-KEY header is missing"}
                return response_formatter(BAD_REQUEST_DEVELOPER_ERROR, data)

            broker_account = self.authenticate_with_api_key()
            if not broker_account:
                data = {"message": "Invalid or inactive X-API-KEY header", "error": "Invalid or inactive X-API-KEY header"}
                return response_formatter(BAD_REQUEST_DEVELOPER_ERROR, data)

            if not request.content_type.startswith("text/plain"):
                data = {"message": "Invalid Content-Type Header", "error": "Invalid Content-Type Header"}
                return response_formatter(BAD_REQUEST_DEVELOPER_ERROR, data)

            if isinstance(request.data, str):
                message = request.data.strip()
            else:
                message = request.data.get("message")

            if not message:
                return response_formatter(BAD_REQUEST_USER_ERROR, {"message": "Signal message is required"})

            signal = self.trading_signal_model.objects.create(
                user=broker_account.user, account=broker_account, raw_message=message
            )

            process_signal_task.delay(signal.id)

            data = {"message": "Signal received", "info": "Signal Received and processing"}
            return response_formatter(SUCCESS_RESPONSE_200, data)

        except Exception as e:
            logger.exception(f"ERROR:---------->>Receive Signal API View error: {e}")
            return response_formatter(INTERNAL_SERVER_ERROR)

    def authenticate_with_api_key(self):
        api_key = self.request.headers.get("X-API-KEY")
        if not api_key:
            return None

        hashed = hash_api_key(api_key)

        try:
            return self.model_class.objects.get(api_key_hash=hashed)
        except self.model_class.DoesNotExist:
            return None
