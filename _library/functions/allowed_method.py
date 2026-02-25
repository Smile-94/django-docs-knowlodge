from collections.abc import Iterable
from functools import wraps

from django.http import JsonResponse

from _library.error_codes import METHOD_NOT_ALLOWED_ERROR


def allowed_methods(*methods: Iterable[str]):
    """
    Class decorator to restrict allowed HTTP methods on Django class-based views.

    This decorator wraps the view's `dispatch` method and returns a standardized
    405 (Method Not Allowed) JSON response when an unsupported HTTP method is used.

    Example:
        @allowed_methods("GET", "POST")
        class MyView(View):
            ...

    Notes:
    - Method names are normalized to uppercase.
    - Adds an HTTP `Allow` header as per RFC 9110.
    - Intended for API-style views returning JSON responses.
    """

    # Normalize once for performance and consistency
    allowed = {method.upper() for method in methods}

    def decorator(cls):
        # Ensure the class has a dispatch method (CBV safety check)
        if not hasattr(cls, "dispatch"):
            raise AttributeError(f"{cls.__name__} must define a 'dispatch' method to use @allowed_methods")

        original_dispatch = cls.dispatch

        @wraps(original_dispatch)
        def wrapped_dispatch(self, request, *args, **kwargs):
            """
            Intercepts the request before dispatch and validates HTTP method.
            """
            if request.method not in allowed:
                METHOD_NOT_ALLOWED_ERROR["data"] = {
                    "url": request.path,
                    "allowed_methods": sorted(allowed),
                    "info": "Use one of the allowed HTTP methods.",
                }
                response = JsonResponse(METHOD_NOT_ALLOWED_ERROR, status=405)

                # RFC-compliant Allow header
                response["Allow"] = ", ".join(sorted(allowed))
                return response

            return original_dispatch(self, request, *args, **kwargs)

        cls.dispatch = wrapped_dispatch
        return cls

    return decorator
