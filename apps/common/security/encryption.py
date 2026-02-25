import hashlib
import secrets

from cryptography.fernet import Fernet
from django.conf import settings


def _get_cipher():
    return Fernet(settings.BROKER_API_ENCRYPTION_KEY)


def generate_raw_api_key(length: int = 48) -> str:
    """
    Generate cryptographically secure random key.
    """
    return secrets.token_urlsafe(length)


def hash_api_key(raw_key: str) -> str:
    """
    Deterministic SHA256 hash for uniqueness check.
    """
    return hashlib.sha256(raw_key.encode()).hexdigest()


def encrypt_api_key(raw_key: str) -> str:
    """
    Encrypt API key before storing.
    """
    cipher = _get_cipher()
    return cipher.encrypt(raw_key.encode()).decode()
