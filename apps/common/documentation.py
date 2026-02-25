from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)

from _library.dataclass import ErrorResponse, SuccessResponse

TAG_NAME = "System"


# <<--------------------------------- System Health Check Documentation --------------------------------->>
class SystemDocumentation:
    @staticmethod
    def health_check():
        return extend_schema(
            tags=[TAG_NAME],
            summary="System Health Check",
            description=(
                "Check system infrastructure health status.\n\n"
                "**Components Checked:**\n"
                "- Database connection\n"
                "- Redis connection\n"
                "- Celery worker availability\n\n"
                "**Response Behavior:**\n"
                "- Returns `healthy` if all services are working\n"
                "- Returns `unhealthy` if any service fails\n"
                "- No authentication required\n"
            ),
            request=None,
            responses={
                # ================= SUCCESS =================
                200: OpenApiResponse(
                    response=SuccessResponse,
                    description="System health status retrieved successfully",
                    examples=[
                        OpenApiExample(
                            name="Healthy System",
                            value={
                                "status": 200,
                                "message": "System are healthy",
                                "data": {
                                    "database": True,
                                    "redis": True,
                                    "celery": True,
                                    "webhook": True,
                                    "status": "healthy",
                                },
                                "links": None,
                            },
                            response_only=True,
                        ),
                        OpenApiExample(
                            name="Unhealthy System",
                            value={
                                "status": 200,
                                "message": "System are unhealthy",
                                "data": {
                                    "database": True,
                                    "redis": False,
                                    "celery": False,
                                    "status": "unhealthy",
                                },
                                "links": None,
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
