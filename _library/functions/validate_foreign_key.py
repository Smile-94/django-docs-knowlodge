from typing import Any, TypedDict

from django.db.models import Model


class ForeignKeyValidationResult(TypedDict):
    instance: Model | None
    invalid_fk: dict | None
    not_exist_fk: dict | None


def validate_foreign_key(
    value: int, field: str, model: type[Model], required: bool = True, **kwargs
) -> ForeignKeyValidationResult:
    """
    Validate a foreign key reference.

    Responsibilities:
    - Validate required constraint
    - Ensure value is a valid integer
    - Ensure referenced object exists
    - Return resolved instance or structured error info
    """

    def _error(message: str) -> dict:
        """Standardized error payload builder."""
        data: dict[str, Any] = {field: value, "info": message}
        index = kwargs.get("index")
        if index is not None:
            data["index"] = index
        return data

    # -------------------------
    # Required field validation
    # -------------------------
    if value in (None, "", 0):
        if required:
            return {"instance": None, "invalid_fk": _error(f"{field} is required"), "not_exist_fk": None}
        return {"instance": None, "invalid_fk": None, "not_exist_fk": None}

    # -------------------------
    # Type normalization
    # -------------------------
    try:
        value = int(value)
    except (TypeError, ValueError):
        return {"instance": None, "invalid_fk": _error(f"{field} must be an integer"), "not_exist_fk": None}

    # -------------------------
    # Database existence check
    # -------------------------
    try:
        instance: Model = model.objects.get(id=value)
    except model.DoesNotExist:
        return {"instance": None, "invalid_fk": None, "not_exist_fk": _error(f"{field} does not exist")}

    # -------------------------
    # Success
    # -------------------------
    return {"instance": instance, "invalid_fk": None, "not_exist_fk": None}
