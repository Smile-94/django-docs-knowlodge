from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)

from _library.dataclass import ErrorResponse, SuccessResponse
from apps.broker.serializers.broker_account_serializer import BrokerAccountSerializer

TAG_NAME = "Broker Account"


# <<--------------------------------- Broker Account Documentation --------------------------------->>
class BrokerAccountDocumentation:
    @staticmethod
    def create():
        return extend_schema(
            tags=[TAG_NAME],
            summary="Create Broker Account",
            description=(
                "Create a broker account for the authenticated user.\n\n"
                "**Key Rules:**\n"
                "- Only authenticated users can create a broker account\n"
                "- Only one broker account is allowed per user\n"
                "- API key is encrypted before storage\n"
                "- API key hash is stored for verification purposes\n"
                "- Operation runs inside an atomic transaction\n"
                "- Unknown fields are rejected\n\n"
                "**Security Model:**\n"
                "- Raw API key is never returned in response\n"
                "- API key is encrypted using server-side encryption\n"
                "- Sensitive data is hashed before persistence\n"
            ),
            request=BrokerAccountSerializer,
            responses={
                # ===================== SUCCESS =====================
                201: OpenApiResponse(
                    response=SuccessResponse,
                    description="Broker account created successfully",
                    examples=[
                        OpenApiExample(
                            name="Successful Broker Creation",
                            value={
                                "status": 201,
                                "message": "Created Broker Account",
                                "data": {"id": 10},
                                "links": None,
                            },
                            response_only=True,
                        )
                    ],
                ),
                # ===================== CLIENT ERRORS =====================
                400: OpenApiResponse(
                    response=ErrorResponse,
                    description="Validation or request error",
                    examples=[
                        OpenApiExample(
                            name="No Request Data",
                            value={
                                "status": 400,
                                "message": "No request data provided",
                            },
                            response_only=True,
                        ),
                        OpenApiExample(
                            name="Invalid Fields",
                            value={
                                "status": 400,
                                "message": "Invalid request fields",
                                "errors": {"unexpected_field": "This field is not allowed"},
                            },
                            response_only=True,
                        ),
                        OpenApiExample(
                            name="Serializer Validation Error",
                            value={
                                "status": 400,
                                "message": "Data Validation Error",
                                "errors": {
                                    "api_key": ["This field is required"],
                                    "broker_name": ["This broker is not supported"],
                                },
                            },
                            response_only=True,
                        ),
                        OpenApiExample(
                            name="Broker Already Exists",
                            value={
                                "status": 400,
                                "message": "Broker account already exists",
                            },
                            response_only=True,
                        ),
                    ],
                ),
                # ===================== AUTH ERROR =====================
                401: OpenApiResponse(
                    response=ErrorResponse,
                    description="Authentication required",
                    examples=[
                        OpenApiExample(
                            name="Unauthorized",
                            value={
                                "status": 401,
                                "message": "Authentication credentials were not provided.",
                            },
                            response_only=True,
                        )
                    ],
                ),
                # ===================== SERVER ERROR =====================
                500: OpenApiResponse(
                    response=ErrorResponse,
                    description="Internal server error",
                    examples=[
                        OpenApiExample(
                            name="Server Error",
                            value={
                                "status": 500,
                                "message": "Internal Server Error",
                            },
                            response_only=True,
                        )
                    ],
                ),
            },
        )
