import logging

from django.utils.timezone import now
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from _library.functions.generate_token import hash_token, validate_token_signature
from apps.user.models.user_model import UserDeviceToken

logger = logging.getLogger(__name__)


class DeviceTokenAuthentication(BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        # 🔹 No auth header → do NOT authenticate, do NOT fail
        if not auth_header:
            return None

        device_id = request.headers.get("X-Device-ID")
        browser_fingerprint = request.headers.get("X-Browser-Fingerprint")
        user_agent = request.META.get("HTTP_USER_AGENT", "")

        # 🔹 Auth header exists but required headers missing → FAIL
        if not device_id or not browser_fingerprint:
            raise AuthenticationFailed("Missing device headers. provide 'X-Device-ID' and 'X-Browser-Fingerprint' in header.")

        try:
            prefix, token = auth_header.split()
        except ValueError:
            raise AuthenticationFailed("Invalid Authorization header format.")

        if prefix != self.keyword:
            raise AuthenticationFailed("Expected Bearer token.")

        raw_token = validate_token_signature(token)
        if not raw_token:
            raise AuthenticationFailed("Invalid token signature.")

        token_hash = hash_token(raw_token)

        try:
            user_token = UserDeviceToken.objects.get(
                access_token_hash=token_hash,
                device_id=device_id,
                is_active=True,
            )
        except UserDeviceToken.DoesNotExist:
            raise AuthenticationFailed("Invalid or inactive token.")

        if user_token.access_expires_at < now():
            raise AuthenticationFailed("Access token expired.")

        if user_token.browser_fingerprint != hash_token(browser_fingerprint):
            raise AuthenticationFailed("Device fingerprint mismatch.")

        if user_token.user_agent_hash != hash_token(user_agent):
            raise AuthenticationFailed("User agent mismatch.")

        return (user_token.user, user_token)
