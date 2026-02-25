from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)

from _library.dataclass import ErrorResponse, SuccessResponse
from apps.user.serializers.registration_serializer import RegistrationSerializer

TAG_NAME = "User"


# <<--------------------------------- Registration Documentation --------------------------------->>
class UserRegistrationDocumentation:
    @staticmethod
    def registration():
        return extend_schema(
            tags=[TAG_NAME],
            summary="User Registration",
            description=(
                "Create a new user account in the system.\n\n"
                "**Key Behaviors:**\n"
                "- Accepts username, email, or phone as unique identifiers\n"
                "- Password is securely hashed before storage\n"
                "- Request fields are strictly validated against allowed model fields\n"
                "- Operation is executed inside an atomic database transaction\n\n"
                "**Security Model:**\n"
                "- Raw passwords are never stored\n"
                "- Unknown or unsafe fields are rejected\n"
                "- Internal errors are not exposed in responses\n"
                "- Supports extension for email/phone verification workflows\n"
            ),
            request=RegistrationSerializer,
            responses={
                # ---------------- Success ----------------
                201: OpenApiResponse(
                    response=SuccessResponse,
                    description="User created successfully",
                    examples=[
                        OpenApiExample(
                            name="Successful Registration",
                            media_type="application/json",
                            status_codes=[201],
                            value={
                                "status": 201,
                                "message": "Created User with id '101'",
                                "data": {"id": 101},
                                "links": None,
                            },
                            response_only=True,
                        )
                    ],
                ),
                # ---------------- Developer Errors ----------------
                400: OpenApiResponse(
                    response=ErrorResponse,
                    description="Invalid request payload or validation failure",
                    examples=[
                        OpenApiExample(
                            name="Missing Request Data",
                            value={
                                "status": 400,
                                "message": "No request data provided",
                            },
                            response_only=True,
                        ),
                        OpenApiExample(
                            name="Invalid Request Fields",
                            value={
                                "status": 400,
                                "message": "Invalid request fields",
                                "errors": {"unexpected_field": "This field is not allowed"},
                            },
                            response_only=True,
                        ),
                        OpenApiExample(
                            name="Validation Error",
                            value={
                                "status": 400,
                                "message": "Data Validation Error",
                                "errors": {"email": ["This email is already in use"], "password": ["Password is too weak"]},
                            },
                            response_only=True,
                        ),
                    ],
                ),
                # ---------------- Server Error ----------------
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
