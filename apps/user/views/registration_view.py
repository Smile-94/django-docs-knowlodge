import logging

from django.db.transaction import atomic
from rest_framework.views import APIView

from _library.error_codes import BAD_REQUEST_DEVELOPER_ERROR, BAD_REQUEST_USER_ERROR, INTERNAL_SERVER_ERROR
from _library.functions.allowed_method import allowed_methods
from _library.functions.formatters import response_formatter
from _library.success_code import SUCCESS_RESPONSE_201
from apps.common.functions.create_instance import create_instance
from apps.common.functions.payload_generator import get_payload_data
from apps.common.functions.validators import validate_request_fields
from apps.user.documentation.registration_documentation import UserRegistrationDocumentation
from apps.user.models.user_model import User
from apps.user.serializers.registration_serializer import RegistrationSerializer

logger = logging.getLogger(__name__)


# <<--------------------------------- Registration View --------------------------------->>
@allowed_methods("POST")
class RegistrationView(APIView):
    authentication_classes = []
    permission_classes = []

    model_class = User
    serializer_class = RegistrationSerializer

    @UserRegistrationDocumentation.registration()
    def post(self, request):
        try:
            # Reject empty payloads early to avoid undefined auth behavior
            if not request.data:
                data = {"message": "No request data provided", "payload": get_payload_data(self.serializer_class)}
                return response_formatter(BAD_REQUEST_DEVELOPER_ERROR, data)

            # Validate Request Fields
            invalid_fields = validate_request_fields(self.model_class, request.data, self.serializer_class)
            if invalid_fields:
                data = {"errors": invalid_fields, "message": "Invalid request fields"}
                return response_formatter(BAD_REQUEST_DEVELOPER_ERROR, data)

            # Initialize serializer with request data (no DB access yet)
            serializer = self.serializer_class(data=request.data)

            # Validate incoming data before any database interaction
            if not serializer.is_valid():
                data = {"errors": serializer.errors, "message": "Data Validation Error"}
                return response_formatter(BAD_REQUEST_USER_ERROR, data)

            with atomic():
                # Create new user instance
                instance = create_instance(self.model_class, serializer.validated_data, extract_fields=["confirm_password"])
                instance.set_password(instance.password)
                instance.save()

                # Minimal response payload to reduce response size
                data = {"id": instance.id, "message": f"Created {self.model_class.__name__} with id '{instance.id}'"}
                return response_formatter(SUCCESS_RESPONSE_201, data)

        except Exception as e:
            logger.exception(f"ERROR:---------->>Registration View error: {e}")
            return response_formatter(INTERNAL_SERVER_ERROR)
