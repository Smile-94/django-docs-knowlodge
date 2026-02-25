import hashlib
import uuid

DEVICE_HEADER = "X-Device-ID"
DEVICE_COOKIE = "device_id"


def get_device_id(request):
    """
    Resolve device identifier from request.
    Priority:
    1. Header
    2. Cookie
    3. Generate new
    """
    # 1. Header (recommended for mobile / API clients)
    device_id = request.headers.get(DEVICE_HEADER)
    if device_id:
        return device_id, False

    # 2. Cookie (browser clients)
    device_id = request.COOKIES.get(DEVICE_COOKIE)
    if device_id:
        return device_id, False

    # 3. Generate new device id
    return str(uuid.uuid4()), True


def get_browser_fingerprint(request) -> str:
    """Generate a simple browser fingerprint"""
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    accept = request.META.get("HTTP_ACCEPT", "")
    encoding = request.META.get("HTTP_ACCEPT_ENCODING", "")
    language = request.META.get("HTTP_ACCEPT_LANGUAGE", "")
    raw = f"{user_agent}|{accept}|{encoding}|{language}"
    return hashlib.sha256(raw.encode()).hexdigest()
