from datetime import date, datetime, time
from enum import Enum
import pytz


class DateTimeTypeChoices(str, Enum):
    """
    Supported return types for current timestamp.

    Used to control whether the function returns:
    - full datetime
    - date only
    - time only
    """

    DATETIME = "datetime"
    DATE = "date"
    TIME = "time"


def get_current_timestamp(
    type: DateTimeTypeChoices = DateTimeTypeChoices.DATETIME, time_zone: str = "Asia/Dhaka"
) -> datetime | date | time:
    """
    Returns the current timestamp based on Django's configured timezone.

    This function is fully timezone-aware and relies on Django's
    `TIME_ZONE` and `USE_TZ` settings.

    Args:
        type (DateTimeTypeChoices):
            Determines the return value:
            - DATETIME → timezone-aware datetime
            - DATE → date only
            - TIME → time only

    Returns:
        datetime | date | time:
            The current timestamp in the requested format.

    Raises:
        ValueError:
            If an unsupported DateTimeTypeChoices value is provided.
    """

    # Get current timezone-aware datetime
    tz = pytz.timezone(time_zone)
    now = datetime.now(tz)

    # Return full datetime
    if type == DateTimeTypeChoices.DATETIME:
        return now

    # Return only date portion
    if type == DateTimeTypeChoices.DATE:
        return now.date()

    # Return only time portion
    if type == DateTimeTypeChoices.TIME:
        return now.time()

    # Defensive programming: fail fast for invalid values
    raise ValueError(f"Invalid date/time type: {type}")


print(get_current_timestamp("datetime"))
