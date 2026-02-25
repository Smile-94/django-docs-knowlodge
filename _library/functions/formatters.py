from copy import deepcopy

from rest_framework.response import Response

from _library.dataclass import ErrorResponse, SuccessResponse


def inject_data_to_code_object(code_object: SuccessResponse | ErrorResponse | dict, data) -> dict:
    """
    Inject dynamic response data into a standardized response object.

    This function safely merges runtime `data` into a response template
    (SuccessResponse / ErrorResponse / dict) without mutating the original
    object. It also supports overriding the response message if provided
    inside the data payload.

    Behavior:
    - Returns the original object if `data` is empty or None.
    - Deep-copies the response template to prevent side effects.
    - Extracts and overrides `message` if present in data.
    - Ensures the final output is always a dictionary with a `data` key.

    Args:
        code_object: Base response template (dataclass or dict).
        data: Payload to be injected into the response.

    Returns:
        dict: Fully constructed response body.
    """
    # If no data is provided, return as-is (no mutation or copy)
    if not data:
        return code_object

    # Avoid mutating shared response templates
    code_object = deepcopy(code_object)

    # Allow dynamic message override from payload
    if isinstance(data, dict) and "message" in data:
        code_object["message"] = data.pop("message")

    # Normalize response object to dict
    if not isinstance(code_object, dict):
        code_object = code_object.model_dump()

    # Attach payload under the standard `data` key
    code_object["data"] = data

    return code_object


def response_formatter(code_object: SuccessResponse | ErrorResponse | dict, data=None) -> Response:
    """
    Construct a DRF `Response` using a standardized response schema.

    This function:
    - Normalizes response objects (dataclass → dict).
    - Injects runtime payload data if provided.
    - Uses the embedded HTTP status code for the response.

    Args:
        code_object: Base response schema containing status and metadata.
        data: Optional payload to include in the response body.

    Returns:
        Response: Django REST Framework response object.
    """
    # Ensure response template is a dictionary
    if not isinstance(code_object, dict):
        code_object = code_object.model_dump()

    # Merge payload into the response schema
    code_object = inject_data_to_code_object(code_object, data)

    # Status code is sourced from the response schema itself
    return Response(code_object, code_object["status"])
