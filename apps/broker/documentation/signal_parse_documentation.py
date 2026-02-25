from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)

from _library.dataclass import ErrorResponse, SuccessResponse

TAG_NAME = "Webhook Signal"


# <<--------------------------------- Receive Signal Documentation --------------------------------->>
class SignalDocumentation:
    @staticmethod
    def receive():
        return extend_schema(
            tags=[TAG_NAME],
            summary="Receive Trading Signal",
            description=(
                "Receive trading signals from broker/webhook system.\n\n"
                "**Authentication:**\n"
                "- Requires `X-API-KEY` header\n"
                "- API key is hashed and validated against stored broker accounts\n"
                "- Request is rejected if API key is missing or invalid\n\n"
                "**Request Requirements:**\n"
                "- Content-Type must be `text/plain`\n"
                "- Signal message must be provided in request body\n"
                "- Accepts raw text or JSON containing `message` field\n\n"
                "**Security Model:**\n"
                "- No sensitive data is returned\n"
                "- API key is never returned\n"
                "- Only validated broker accounts can send signals\n"
            ),
            request=None,  # PlainTextParser → No serializer-based request
            responses={
                # ================= SUCCESS =================
                200: OpenApiResponse(
                    response=SuccessResponse,
                    description="Signal received successfully",
                    examples=[
                        OpenApiExample(
                            name="Signal Received",
                            value={
                                "status": 200,
                                "message": "Signal received",
                                "data": {"info": "Signal Received and processing"},
                                "links": None,
                            },
                            response_only=True,
                        ),
                        OpenApiExample(
                            name="Example Trading Signal",
                            value="""BUY EURUSD [@1.0860 - Optional]

                            SL 1.0850
                            TP 1.0890
                            """,
                            description="Example of a valid trading signal body sent as text/plain",
                            request_only=True,
                        ),
                    ],
                ),
                # ================= CLIENT ERRORS =================
                400: OpenApiResponse(
                    response=ErrorResponse,
                    description="Bad request or authentication failure",
                    examples=[
                        OpenApiExample(
                            name="Missing API Key",
                            value={
                                "status": 400,
                                "message": "No X-API-KEY header provided",
                                "error": "X-API-KEY header is missing",
                            },
                            response_only=True,
                        ),
                        OpenApiExample(
                            name="Invalid API Key",
                            value={
                                "status": 400,
                                "message": "Invalid or inactive X-API-KEY header",
                                "error": "Invalid or inactive X-API-KEY header",
                            },
                            response_only=True,
                        ),
                        OpenApiExample(
                            name="Invalid Content-Type",
                            value={
                                "status": 400,
                                "message": "Invalid Content-Type Header",
                                "error": "Invalid Content-Type Header",
                            },
                            response_only=True,
                        ),
                        OpenApiExample(
                            name="Missing Signal Message",
                            value={
                                "status": 400,
                                "message": "Signal message is required",
                            },
                            response_only=True,
                        ),
                    ],
                ),
                # ================= SERVER ERROR =================
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
