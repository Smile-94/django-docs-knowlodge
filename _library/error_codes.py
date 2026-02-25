from rest_framework import status

from _library.dataclass import ErrorResponse, ErrorType, ResponseClient

# 404 NOT FOUND
NOT_FOUND_ERROR = ErrorResponse(
    status=status.HTTP_404_NOT_FOUND,
    type=ErrorType.ERROR,
    message="404 Page Not Found",
    client=ResponseClient.DEVELOPER,
    data={},
).model_dump()

# 400 BAD REQUEST
BAD_REQUEST_DEVELOPER_ERROR = ErrorResponse(
    status=status.HTTP_400_BAD_REQUEST,
    type=ErrorType.ERROR,
    message="400 Bad Request",
    client=ResponseClient.DEVELOPER,
    data={},
).model_dump()

# 400 BAD REQUEST
BAD_REQUEST_USER_ERROR = ErrorResponse(
    status=status.HTTP_400_BAD_REQUEST,
    type=ErrorType.ERROR,
    message="400 Bad Request",
    client=ResponseClient.USER,
    data={},
).model_dump()

# 401 UNAUTHORIZED
UNAUTHORIZED_ERROR = ErrorResponse(
    status=status.HTTP_401_UNAUTHORIZED,
    type=ErrorType.ERROR,
    message="401 Unauthorized",
    client=ResponseClient.DEVELOPER,
    data={},
).model_dump()

# 403 FORBIDDEN
FORBIDDEN_ERROR = ErrorResponse(
    status=status.HTTP_403_FORBIDDEN,
    type=ErrorType.ERROR,
    message="403 Forbidden",
    client=ResponseClient.DEVELOPER,
    data={},
).model_dump()

# 405 METHOD NOT ALLOWED
METHOD_NOT_ALLOWED_ERROR = ErrorResponse(
    status=status.HTTP_405_METHOD_NOT_ALLOWED,
    type=ErrorType.ERROR,
    message="405 Method Not Allowed",
    client=ResponseClient.DEVELOPER,
    data={},
).model_dump()

# 406 NOT ACCEPTABLE
NOT_ACCEPTABLE_ERROR = ErrorResponse(
    status=status.HTTP_406_NOT_ACCEPTABLE,
    type=ErrorType.ERROR,
    message="406 Not Acceptable",
    client=ResponseClient.DEVELOPER,
    data={},
).model_dump()

# 409 CONFLICT
CONFLICT_ERROR = ErrorResponse(
    status=status.HTTP_409_CONFLICT,
    type=ErrorType.ERROR,
    message="409 Conflict",
    client=ResponseClient.DEVELOPER,
    data={},
).model_dump()

# 500 INTERNAL SERVER ERROR
INTERNAL_SERVER_ERROR = ErrorResponse(
    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    type=ErrorType.ERROR,
    message="500 Internal Server Error",
    client=ResponseClient.DEVELOPER,
    data={},
).model_dump()

# 503 SERVICE UNAVAILABLE
SERVICE_UNAVAILABLE_ERROR = ErrorResponse(
    status=status.HTTP_503_SERVICE_UNAVAILABLE,
    type=ErrorType.ERROR,
    message="503 Service Unavailable",
    client=ResponseClient.DEVELOPER,
    data={},
).model_dump()
