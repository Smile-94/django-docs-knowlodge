from enum import Enum


class DateTimeTypeChoices(str, Enum):
    # Supported date/time types
    DATETIME = "datetime"
    DATE = "date"
    TIME = "time"


def timestamp(value: str, type: DateTimeTypeChoices) -> str:
    # Convert string to datetime
    if type == DateTimeTypeChoices.DATETIME:
        return value
    elif type == DateTimeTypeChoices.DATE:
        return value
    elif type == DateTimeTypeChoices.TIME:
        return value
    else:
        raise ValueError(f"Invalid date/time type: {type}")
