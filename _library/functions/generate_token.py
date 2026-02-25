from datetime import timedelta
import hashlib
import hmac
import secrets

from django.conf import settings
from django.utils import timezone


def generate_raw_token() -> str:
    """Generate a secure, HMAC-signed opaque token"""
    raw = secrets.token_urlsafe(64)
    signature = hmac.new(settings.TOKEN_SECRET_KEY.encode(), raw.encode(), hashlib.sha256).hexdigest()
    return f"{raw}.{signature}"


def hash_token(token: str) -> str:
    """Hash a token for storing in DB"""
    return hashlib.sha256(token.encode()).hexdigest()


def validate_token_signature(token: str) -> str | None:
    """Validate HMAC signature and return full token"""
    try:
        raw, signature = token.rsplit(".", 1)
        expected = hmac.new(settings.TOKEN_SECRET_KEY.encode(), raw.encode(), hashlib.sha256).hexdigest()
        if hmac.compare_digest(signature, expected):
            return token
    except Exception:
        return None
    return None


def get_access_token_expiry():
    return timezone.now() + timedelta(seconds=settings.ACCESS_TOKEN_TTL)


def get_refresh_token_expiry():
    return timezone.now() + timedelta(seconds=settings.REFRESH_TOKEN_TTL)
