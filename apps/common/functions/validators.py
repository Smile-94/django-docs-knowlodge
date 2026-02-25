from collections.abc import Iterable
import logging
from typing import Any

from django.core.exceptions import FieldDoesNotExist
from django.db.models import Model
from rest_framework.request import Request
from rest_framework.serializers import Serializer

logger = logging.getLogger(__name__)


def validate_device_headers(request: Request, extended_header=None) -> tuple[bool, dict[str, Any] | None]:
    """
    Validate required security headers from the incoming request.

    This function checks whether the required device-identifying headers
    are present in the HTTP request. These headers are typically used
    for refresh token validation, device binding, and enhanced security.

    Required Headers:
        - X-Device-ID
        - X-Browser-Fingerprint

    Args:
        request (Request): DRF request object.

    Returns:
        Tuple[bool, Optional[Dict[str, Any]]]:
            - True, None → If all required headers exist.
            - False, error_data → If any required header is missing.
    """

    required_headers = ["X-Device-ID", "X-Browser-Fingerprint"]
    missing_headers = []

    if extended_header:
        required_headers.append(extended_header)

    for header in required_headers:
        if not request.headers.get(header):
            missing_headers.append(header)

    if missing_headers:
        return False, {
            "message": "Missing required security headers",
            "info": f"Missing headers: {', '.join(missing_headers)}",
        }

    return True, None


def validate_request_fields(
    model_class: type[Model],
    request_data: dict[str, Any],
    serializer_class: type[Serializer] | None = None,
    extended_fields: Iterable[str] | None = None,
) -> Iterable[str]:
    """
    Validate incoming request fields against:
    - Django model fields
    - DRF serializer fields (if provided)
    - Optional extended/custom fields

    Returns:
        List[str]: List of invalid fields found in request_data.
                   Empty list if all fields are valid.

    Notes:
        This function does NOT raise ValidationError automatically.
        It logs any exceptions and returns invalid fields for further handling.
    """
    try:
        # 1. Collect model field names
        model_fields = {field.name for field in model_class._meta.fields}

        # 2. Collect serializer fields (if provided)
        serializer_fields = set()
        if serializer_class:
            serializer_fields = set(serializer_class().get_fields().keys())

        # 3. Include extended/custom fields
        extra_fields = set(extended_fields or [])

        # 4. Build final allowed fields set
        allowed_fields = model_fields | serializer_fields | extra_fields

        # 5. Detect invalid fields
        invalid_fields = [field for field in request_data.keys() if field not in allowed_fields]

        return invalid_fields

    except FieldDoesNotExist as e:
        # Log model field errors and return as invalid field
        logger.exception(f"Model field does not exist: {e}")
        return [str(e)]

    except Exception as e:
        # Log unexpected errors and return a descriptive invalid field
        logger.exception(f"Unexpected error validating request fields: {e}")
        return [f"Unexpected error: {str(e)}"]


def validate_field_list(field_list, serializer_class=None, model_class=None):
    """
    Validate field_list against serializer/model fields.

    Returns:
        tuple[list[str] | str, list[str]]
        → (validated_field_list, invalid_fields)
    """
    if field_list == "*":
        return None

    allowed_fields = set()

    if serializer_class:
        allowed_fields |= set(serializer_class().get_fields().keys())

    if model_class:
        allowed_fields |= {field.name for field in model_class._meta.get_fields()}

    invalid_fields = sorted(set(field_list) - allowed_fields)

    return invalid_fields


def validate_query_params(
    request, query_filter: dict | None = None, query_type="list", extended_fields: list[str] | None = None
) -> tuple[list[str], list[str]]:
    """
    Validate query params from request.

    Args:
        request: DRF request object
        query_filter: dict mapping valid query param keys to model fields
        extra_valid_fields: additional fields to consider valid

    Returns:
        tuple:
            valid_params: list of keys that are valid
            invalid_params: list of keys that are invalid
    """
    if query_type == "list":
        # Default query params always allowed
        default_fields = {"field_list", "from_date", "to_date", "search", "limit", "offset"}
    elif query_type == "retrieve":
        # Default query params always allowed
        default_fields = {"field_list"}

    elif query_type == "create":
        # Default query params always allowed
        default_fields = {}

    # Combine defaults + query_filter keys + extra valid fields
    valid_fields = set(default_fields) | set(query_filter.keys()) if query_filter else set(default_fields)
    if extended_fields:
        valid_fields |= set(extended_fields)

    # Extract params from request
    provided_fields = set(request.query_params.keys())

    # Determine valid and invalid
    valid_params = list(valid_fields)
    invalid_params = list(provided_fields - valid_fields)

    return valid_params, invalid_params
