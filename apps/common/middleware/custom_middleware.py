import logging
import time

from django.http import JsonResponse
from django.urls import Resolver404, resolve
from rest_framework import status
from rest_framework.request import Request

from _library.error_codes import NOT_FOUND_ERROR
from apps.common.functions.request_log import get_request_log

logger = logging.getLogger(__name__)


class CacheRequestBodyMiddleware:
    """
    Ensures request.body is cached early, preventing RawPostDataException.
    Must be placed at the top of MIDDLEWARE.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only cache for methods that typically have a body
        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            try:
                # Cache raw body early to avoid DRF RawPostDataException
                if not hasattr(request, "_cached_body"):
                    request._cached_body = request.body  # store raw bytes
            except Exception as e:
                # Log if needed, but continue – the body may be unreadable
                logger.debug(f"Could not cache request body: {e}")
        return self.get_response(request)


class UrlValidationMiddleware:
    """
    Middleware to check if the request URL exists.
    If not, returns a 404 Page Not Found response using InvalidUrlResponse model.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Attempt to resolve the URL path
            resolve(request.path)

        except Resolver404:
            # Create the response using the InvalidUrlResponse model
            NOT_FOUND_ERROR["data"] = {"url": request.path, "info": "The requested URL does not exist."}
            return JsonResponse(NOT_FOUND_ERROR, status=status.HTTP_404_NOT_FOUND)

        # If the URL is valid, continue processing the request
        response = self.get_response(request)
        return response


class RequestLoggingMiddleware:
    """
    Middleware to log every incoming request using get_log_request().
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Only wrap DRF Request for API endpoints
            try:
                resolver_match = resolve(request.path)
                is_api = resolver_match.app_name == "api" or request.path.startswith("/api/")
            except Exception:
                is_api = False

            if is_api:
                # Trigger DRF authentication for API requests
                drf_request = Request(request)
                _ = getattr(drf_request, "user", None)  # forces authentication
                request.drf_request = drf_request
            else:
                drf_request = request  # leave Django request as-is
            # Continue processing the request
            response = self.get_response(request)

            # Log the request
            get_request_log(request)
            return response
        except Exception as e:
            logger.exception(f"ERROR:----------->> Request Logging Middleware error: {e}")


class RequestTimingMiddleware:
    """
    Logs request + execution time
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.perf_counter()

        response = self.get_response(request)

        end_time = time.perf_counter()
        execution_time = round((end_time - start_time) * 1000, 2)  # ms

        logger.info(
            f"INFO:----------->> EXECUTION LOG: "
            f"path={request.path}, "
            f"method={request.method}, "
            f"status={response.status_code}, "
            f"execution_time={execution_time}ms"
        )

        return response


class AddCspNonceMiddleware:
    """
    Add a default csp_nonce attribute to the request
    so templates that expect it don't break.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If django-csp is not used, just set empty string
        request.csp_nonce = getattr(request, "csp_nonce", "")
        response = self.get_response(request)
        return response
