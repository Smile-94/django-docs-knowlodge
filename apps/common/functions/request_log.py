from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)

SENSITIVE_HEADERS = {
    "HTTP_AUTHORIZATION",
    "HTTP_X_CSRFTOKEN",
    "HTTP_X_CSRF_TOKEN",
    "HTTP_CSRFTOKEN",
    "HTTP_X_BROWSER_FINGERPRINT",
    "HTTP_X_DEVICE_ID",
    "HTTP_COOKIE",
}

SENSITIVE_BODY_FIELDS = {"password", "confirm_password", "token", "access", "refresh", "api_key"}


def mask_sensitive_body(data):
    if isinstance(data, dict):
        return {k: ("[REDACTED]" if k.lower() in SENSITIVE_BODY_FIELDS else mask_sensitive_body(v)) for k, v in data.items()}
    if isinstance(data, list):
        return [mask_sensitive_body(item) for item in data]
    return data


def get_request_log(request, message="Request Log"):
    user = request.user if hasattr(request, "user") and request.user.is_authenticated else "Anonymous"

    #  Headers
    headers = {k: v for k, v in request.META.items() if k.startswith("HTTP_")}
    for key in headers:
        if key in SENSITIVE_HEADERS:
            headers[key] = "[REDACTED]"

    body_data = {}
    try:
        if request._cached_body:
            try:
                body_data = json.loads(request._cached_body.decode("utf-8"))
            except Exception:
                # Fallback: leave as raw string
                body_data = request._cached_body.decode("utf-8")
        else:
            body_data = {}

        # If DRF request.data exists, use it (already parsed)
        if hasattr(request, "data") and request.data is not None:
            body_data = request.data

        # Mask sensitive fields
        if isinstance(body_data, (dict, list)):
            body_data = mask_sensitive_body(body_data)

    except json.JSONDecodeError:
        body_data = "[UNPARSABLE BODY]"
    except Exception:
        body_data = "[UNPARSABLE BODY]"

    # Mask sensitive fields
    if body_data and isinstance(body_data, (dict, list)):
        body_data = mask_sensitive_body(body_data)

    log_data = {
        "message": message,
        "user": str(user),
        "device": request.META.get("HTTP_USER_AGENT", "Unknown Device"),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "method": request.method,
        "path": request.path,
        "ip_address": request.META.get("REMOTE_ADDR"),
        "headers": headers,
        "request_body": body_data,
        "query_params": request.GET.dict(),
    }

    logger.info(f"INFO:----------->> REQUEST LOG: {log_data}")
    return request
