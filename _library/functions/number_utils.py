from decimal import ROUND_HALF_UP, Decimal
from typing import TypedDict


class IntValidationResult(TypedDict):
    value: int | None
    error: dict | None


def validate_int(
    value: int | str, field: str, default: int | None = 0, min_value: int | None = None, max_value: int | None = None, **kwargs
) -> IntValidationResult:
    """
    Validate and normalize an integer value.

    Stateless, reusable, and safe for bulk validation.
    """

    def error(message: str) -> dict:
        data = {field: value, "info": message}
        index = kwargs.get("index")
        if index is not None:
            data["index"] = index
        return data

    # -------------------------
    # Empty value handling
    # -------------------------
    if value in (None, ""):
        return {"value": default, "error": f"{field} is required"}

    # -------------------------
    # Type normalization
    # -------------------------
    try:
        value = int(value)
    except (TypeError, ValueError):
        return {"value": None, "error": error(f"{field} must be an integer")}

    # -------------------------
    # Min boundary
    # -------------------------
    if min_value is not None and value < min_value:
        return {"value": None, "error": error(f"{field} must be ≥ {min_value}")}

    # -------------------------
    # Max boundary
    # -------------------------
    if max_value is not None and value > max_value:
        return {"value": None, "error": error(f"{field} must be ≤ {max_value}")}

    return {"value": value, "error": None}


def round_half_up(value: float | Decimal, places: int = 2) -> Decimal:
    """
    Round a number using "round half up" method.

    Args:
        value (float | Decimal): The number to round.
        places (int): Number of decimal places to keep (default: 2).

    Returns:
        Decimal: Rounded number.

    Example:
        round_half_up(2.345, 2) -> Decimal('2.35')
        round_half_up(-2.555, 2) -> Decimal('-2.56')
    """
    if not isinstance(value, Decimal):
        value = Decimal(str(value))

    quantize_str = f"1.{'0' * places}"  # e.g. '1.00' for 2 decimal places
    return value.quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)
