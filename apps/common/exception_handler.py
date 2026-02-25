from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exc, context):
    """
    Centralized DRF exception handler.
    Ensures consistent API error responses.
    """
    response = drf_exception_handler(exc, context)

    if response is None:
        return Response(
            {
                "success": False,
                "error": "server_error",
                "detail": "Internal server error",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    response.data = {
        "success": False,
        "error": response.status_code,
        "detail": response.data,
    }

    return response
