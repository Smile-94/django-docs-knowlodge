import logging

from django.contrib.auth import authenticate
from django.utils.timezone import now
from rest_framework.views import APIView

from _library.error_codes import BAD_REQUEST_DEVELOPER_ERROR, BAD_REQUEST_USER_ERROR, INTERNAL_SERVER_ERROR, UNAUTHORIZED_ERROR
from _library.functions.allowed_method import allowed_methods
from _library.functions.device import get_browser_fingerprint, get_device_id
from _library.functions.formatters import response_formatter
from _library.functions.generate_token import (
    generate_raw_token,
    get_access_token_expiry,
    get_refresh_token_expiry,
    hash_token,
    validate_token_signature,
)
from _library.success_code import SUCCESS_RESPONSE_200, SUCCESS_RESPONSE_201
from apps.common.functions.payload_generator import get_payload_data
from apps.common.functions.validators import validate_device_headers
from apps.user.documentation.login_documentation import AuthenticationDocumentation
from apps.user.models.user_model import UserDeviceToken
from apps.user.serializers.login_serializer import LoginSerializer, RefreshTokenSerializer
from apps.user.tasks.invalid_token_task import deactivate_previous_device_sessions

logger = logging.getLogger(__name__)


# <<--------------------------------- Login View --------------------------------->>
@allowed_methods("POST")
class TokenObtainView(APIView):
    authentication_classes = []
    permission_classes = []

    model_class = UserDeviceToken
    serializer_class = LoginSerializer

    @AuthenticationDocumentation.login()
    def post(self, request):
        try:
            # Reject empty payloads early to avoid undefined auth behavior
            if not request.data:
                data = {"message": "No request data provided", "payload": get_payload_data(self.serializer_class)}
                return response_formatter(BAD_REQUEST_DEVELOPER_ERROR, data)

            # Device identity enables per-device session control & revocation
            device_id, is_new_device = get_device_id(request)

            user_agent = request.META.get("HTTP_USER_AGENT", "")
            browser_fingerprint = get_browser_fingerprint(request)

            serializer = self.serializer_class(data=request.data)

            # Validate input before touching auth or persistence layers
            if not serializer.is_valid():
                data = {"errors": serializer.errors, "message": "Data Validation Error"}
                return response_formatter(BAD_REQUEST_USER_ERROR, data)

            # Authenticate credentials without leaking account existence
            user = authenticate(
                username=serializer.validated_data.get("username"),
                password=serializer.validated_data.get("password"),
            )
            if not user:
                data = {"message": "Invalid credentials", "payload": get_payload_data(self.serializer_class)}
                return response_formatter(UNAUTHORIZED_ERROR, data)

            # Raw tokens are generated once and never stored directly
            raw_access = generate_raw_token()
            raw_refresh = generate_raw_token()

            # Hashing prevents token reuse if database is compromised
            access_hash = hash_token(raw_access)
            refresh_hash = hash_token(raw_refresh)

            # Fingerprint & UA are hashed to avoid storing trackable raw values
            fingerprint_hash = hash_token(browser_fingerprint)
            ua_hash = hash_token(user_agent)

            token = self.model_class.objects.create(
                user=user,
                device_id=device_id,
                access_token_hash=access_hash,
                refresh_token_hash=refresh_hash,
                browser_fingerprint=fingerprint_hash,
                user_agent_hash=ua_hash,
                user_agent=user_agent,
                ip_address=request.META.get("REMOTE_ADDR"),
                access_expires_at=get_access_token_expiry(),
                refresh_expires_at=get_refresh_token_expiry(),
            )
            # Enforce single active session per device in background
            deactivate_previous_device_sessions.delay(token.id, user.id, device_id)

            data = {
                "message": "Login successful",
                "access_token": raw_access,
                "refresh_token": raw_refresh,
                "device_id": device_id,
                "browser_fingerprint": browser_fingerprint,
            }

            response = response_formatter(SUCCESS_RESPONSE_201, data)

            # HttpOnly cookie allows device recognition without JS exposure
            if is_new_device:
                response.set_cookie(
                    key="device_id", value=device_id, max_age=60 * 60 * 24 * 365, httponly=True, secure=True, samesite="Lax"
                )

            return response

        except Exception as e:
            logger.exception(f"ERROR:---------->>Login View error: {e}")
            return response_formatter(INTERNAL_SERVER_ERROR)


# <<--------------------------------- Refresh Token View --------------------------------->>
@allowed_methods("POST")
class TokenRefreshView(APIView):
    authentication_classes = []
    permission_classes = []
    model_class = UserDeviceToken
    serializer_class = RefreshTokenSerializer

    @AuthenticationDocumentation.refresh_token()
    def post(self, request):
        try:
            # Reject empty payloads early to avoid undefined auth behavior
            if not request.data:
                data = {"message": "No request data provided", "payload": get_payload_data(self.serializer_class)}
                return response_formatter(BAD_REQUEST_DEVELOPER_ERROR, data)

            # Device and fingerprint must always be present to validate the refresh token
            is_valid, error_data = validate_device_headers(request)

            if not is_valid:
                return response_formatter(BAD_REQUEST_DEVELOPER_ERROR, error_data)

            # Validate input using serializer
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                data = {"errors": serializer.errors, "message": "Data Validation Error"}
                return response_formatter(BAD_REQUEST_USER_ERROR, data)

            refresh_token = serializer.validated_data.get("refresh_token")
            #  Extract device context from headers
            user_agent = request.META.get("HTTP_USER_AGENT", "")
            browser_fingerprint = request.headers.get("X-Browser-Fingerprint")
            device_id = request.headers.get("X-Device-ID")

            # Validate token signature (detect tampering or expiration)
            raw_refresh = validate_token_signature(refresh_token)
            if not raw_refresh:
                data = {"message": "Invalid or expired refresh token", "refresh_token": refresh_token}
                return response_formatter(UNAUTHORIZED_ERROR, data)

            refresh_hash = hash_token(raw_refresh)

            # Fetch the active token for this device
            try:
                token_obj = UserDeviceToken.objects.get(refresh_token_hash=refresh_hash, device_id=device_id, is_active=True)
            except UserDeviceToken.DoesNotExist:
                data = {"message": "Invalid or inactive refresh token", "refresh_token": refresh_token}
                return response_formatter(UNAUTHORIZED_ERROR, data)

            # Check for token expiry
            if token_obj.refresh_expires_at < now():
                token_obj.is_active = False
                token_obj.save(update_fields=["is_active"])
                data = {
                    "message": "Refresh token expired",
                    "refresh_token": refresh_token,
                    "refresh_expires_at": token_obj.refresh_expires_at,
                }
                return response_formatter(UNAUTHORIZED_ERROR, data)

            # Device binding: fingerprint must match the one stored on login
            if token_obj.browser_fingerprint != hash_token(browser_fingerprint):
                data = {
                    "message": "Device fingerprint mismatch",
                    "refresh_token": refresh_token,
                    "browser_fingerprint": browser_fingerprint,
                    "info": "This device fingerprint does not match the one used to issue the refresh token",
                }
                return response_formatter(UNAUTHORIZED_ERROR, data)

            # User agent binding: ensures token is used by same browser
            if token_obj.user_agent_hash != hash_token(user_agent):
                data = {
                    "message": "User agent mismatch",
                    "refresh_token": refresh_token,
                    "user_agent": user_agent,
                    "info": "This user agent does not match the one used to issue the refresh token",
                }
                return response_formatter(UNAUTHORIZED_ERROR, data)

            # Rotate tokens: issue new access & refresh tokens, hash them, update expiry
            new_access = generate_raw_token()
            new_refresh = generate_raw_token()

            token_obj.access_token_hash = hash_token(new_access)
            token_obj.refresh_token_hash = hash_token(new_refresh)
            token_obj.access_expires_at = get_access_token_expiry()
            token_obj.refresh_expires_at = get_refresh_token_expiry()
            token_obj.rotated_at = now()
            token_obj.save()

            data = {"message": "Refresh token rotated", "access_token": new_access, "refresh_token": new_refresh}

            return response_formatter(SUCCESS_RESPONSE_200, data)

        except Exception as e:
            logger.exception(f"ERROR:---------->>Refresh token error {e}")
            return response_formatter(INTERNAL_SERVER_ERROR)
