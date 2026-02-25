from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)

from _library.dataclass import ErrorResponse, SuccessResponse
from apps.user.serializers.login_serializer import LoginSerializer, RefreshTokenSerializer

TAG_NAME = "Authentication"


# <<--------------------------------- Login Documentation --------------------------------->>
class AuthenticationDocumentation:
    @staticmethod
    def login():
        return extend_schema(
            tags=["Authentication"],
            summary="Obtain Access & Refresh Tokens",
            description=(
                "Authenticate a user using username and password and issue "
                "device-bound access and refresh tokens.\n\n"
                "**Key Behaviors:**\n"
                "- Tokens are issued per device\n"
                "- Only one active session is allowed per user-device pair\n"
                "- Previous tokens for the same device are invalidated on login\n\n"
                "**Security Model:**\n"
                "- Tokens are bound to a verified device and browser fingerprint\n"
                "- Raw tokens are returned once and never stored\n"
                "- All persisted secrets are stored as hashes\n"
            ),
            request=LoginSerializer,
            parameters=[
                # ---------------- Device Identification ----------------
                OpenApiParameter(
                    name="X-Device-ID",
                    type=str,
                    location=OpenApiParameter.HEADER,
                    required=False,
                    description=(
                        "Optional device identifier used to associate the login request with an existing device.\n\n"
                        "If provided, the server attempts to reuse the device context and invalidate any "
                        "previous active session for this device.\n\n"
                        "If omitted, a new device identifier is generated and returned in the response "
                        "(and may also be persisted as an HttpOnly cookie).\n\n"
                        "Used for:\n"
                        "- Per-device session tracking\n"
                        "- Token invalidation for the same device\n"
                        "- Secure multi-device login management\n"
                    ),
                    examples=[
                        OpenApiExample(
                            "Existing Device ID",
                            value="834fa6c6-e7c3-4437-9dc5-05b6d406bb2f",
                        ),
                    ],
                ),
            ],
            responses={
                # ---------------- Success ----------------
                201: OpenApiResponse(
                    response=SuccessResponse,
                    description="Authentication successful",
                    examples=[
                        OpenApiExample(
                            name="Successful Login",
                            media_type="application/json",
                            status_codes=[201],
                            value={
                                "status": 201,
                                "message": "Login successful",
                                "client": "user",
                                "data": {
                                    "access_token": "raw_access_token_value",
                                    "refresh_token": "raw_refresh_token_value",
                                    "device_id": "834fa6c6-e7c3-4437-9dc5-05b6d406bb2f",
                                    "browser_fingerprint": "11808ec5f5e1f135c79556a7ee641de4bde02a1a432a45e6b290f1332e5ac105",
                                },
                                "links": None,
                            },
                            response_only=True,
                        )
                    ],
                ),
                # ---------------- Validation Errors ----------------
                400: OpenApiResponse(
                    response=ErrorResponse,
                    description="Invalid request payload",
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
                            name="Validation Error",
                            value={
                                "status": 400,
                                "message": "Data Validation Error",
                                "errors": {
                                    "username": ["This field is required"],
                                    "password": ["This field is required"],
                                },
                            },
                            response_only=True,
                        ),
                    ],
                ),
                # ---------------- Authentication Failure ----------------
                401: OpenApiResponse(
                    response=ErrorResponse,
                    description="Invalid credentials",
                    examples=[
                        OpenApiExample(
                            name="Invalid Credentials",
                            value={
                                "status": 401,
                                "message": "Invalid credentials",
                            },
                            response_only=True,
                        )
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

    @staticmethod
    def refresh_token():
        return extend_schema(
            tags=["Authentication"],
            summary="Rotate Access & Refresh Tokens",
            description=(
                "Rotate access and refresh tokens for a user using a valid refresh token.\n\n"
                "**Key Behaviors:**\n"
                "- Tokens are bound to a specific device and browser fingerprint\n"
                "- Refresh token must be active and not expired\n"
                "- Device and user-agent binding are enforced\n"
                "- Old tokens are replaced with newly generated tokens\n\n"
                "**Security Considerations:**\n"
                "- Raw tokens are returned only once\n"
                "- Only hashed tokens are stored\n"
                "- Requests with invalid headers, mismatched device, or fingerprint are rejected"
            ),
            parameters=[
                # ---------------- Device Identification ----------------
                OpenApiParameter(
                    name="X-Device-ID",
                    type=str,
                    location=OpenApiParameter.HEADER,
                    required=True,
                    description=(
                        "Device identifier associated with the issued refresh token.\n"
                        "Used to enforce per-device session control and token rotation.\n"
                        "Requests without this header or with mismatched device IDs will be rejected."
                    ),
                    examples=[OpenApiExample("Device ID", value="834fa6c6-e7c3-4437-9dc5-05b6d406bb2f")],
                ),
                # ---------------- Browser Fingerprint ----------------
                OpenApiParameter(
                    name="X-Browser-Fingerprint",
                    type=str,
                    location=OpenApiParameter.HEADER,
                    required=True,
                    description=(
                        "Hashed browser fingerprint generated during login.\n"
                        "Used to prevent token replay from another browser/device.\n"
                        "Requests with mismatched fingerprints will be rejected."
                    ),
                    examples=[
                        OpenApiExample("Fingerprint", value="11808ec5f5e1f135c79556a7ee641de4bde02a1a432a45e6b290f1332e5ac105")
                    ],
                ),
            ],
            request=RefreshTokenSerializer,
            responses={
                # ---------------- Success ----------------
                200: OpenApiResponse(
                    response=SuccessResponse,
                    description="Refresh token successfully rotated",
                    examples=[
                        OpenApiExample(
                            name="Success Response",
                            media_type="application/json",
                            status_codes=[200],
                            value={
                                "status": 200,
                                "message": "Refresh token rotated",
                                "client": "user",
                                "data": {"access_token": "new_raw_access_token", "refresh_token": "new_raw_refresh_token"},
                                "links": None,
                            },
                            response_only=True,
                        )
                    ],
                ),
                # ---------------- Validation Errors ----------------
                400: OpenApiResponse(
                    response=ErrorResponse,
                    description="Missing or invalid request data / headers",
                    examples=[
                        OpenApiExample(
                            name="Empty Payload", value={"status": 400, "message": "No request data provided"}, response_only=True
                        ),
                        OpenApiExample(
                            name="Missing Headers",
                            value={
                                "status": 400,
                                "message": "Missing X-Device-ID or X-Browser-Fingerprint header",
                                "info": "X-Device-ID, X-Browser-Fingerprint header missing",
                            },
                            response_only=True,
                        ),
                        OpenApiExample(
                            name="Invalid Input",
                            value={
                                "status": 400,
                                "message": "Data Validation Error",
                                "errors": {"refresh_token": ["This field is required"]},
                            },
                            response_only=True,
                        ),
                    ],
                ),
                # ---------------- Unauthorized ----------------
                401: OpenApiResponse(
                    response=ErrorResponse,
                    description="Invalid, expired, or mismatched refresh token",
                    examples=[
                        OpenApiExample(
                            name="Token Signature Invalid",
                            value={
                                "status": 401,
                                "message": "Invalid or expired refresh token",
                                "refresh_token": "old_token_value",
                            },
                            response_only=True,
                        ),
                        OpenApiExample(
                            name="Inactive Token",
                            value={
                                "status": 401,
                                "message": "Invalid or inactive refresh token",
                                "refresh_token": "old_token_value",
                            },
                            response_only=True,
                        ),
                        OpenApiExample(
                            name="Expired Token",
                            value={
                                "status": 401,
                                "message": "Refresh token expired",
                                "refresh_token": "old_token_value",
                                "refresh_expires_at": "2026-02-06T10:00:00Z",
                            },
                            response_only=True,
                        ),
                        OpenApiExample(
                            name="Device Fingerprint Mismatch",
                            value={
                                "status": 401,
                                "message": "Device fingerprint mismatch",
                                "refresh_token": "old_token_value",
                                "browser_fingerprint": "client_fingerprint",
                            },
                            response_only=True,
                        ),
                        OpenApiExample(
                            name="User Agent Mismatch",
                            value={
                                "status": 401,
                                "message": "User agent mismatch",
                                "refresh_token": "old_token_value",
                                "user_agent": "Mozilla/5.0 ...",
                            },
                            response_only=True,
                        ),
                    ],
                ),
                # ---------------- Server Error ----------------
                500: OpenApiResponse(
                    response=ErrorResponse,
                    description="Unhandled server error",
                    examples=[
                        OpenApiExample(
                            name="Server Error", value={"status": 500, "message": "Internal Server Error"}, response_only=True
                        )
                    ],
                ),
            },
        )
