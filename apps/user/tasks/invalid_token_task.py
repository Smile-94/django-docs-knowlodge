import logging

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.user.models.user_model import UserDeviceToken

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def deactivate_previous_device_sessions(self, token_id, user_id: int, device_id: str) -> int:
    try:
        # Input Validation (Fail Fast)

        if not user_id:
            raise ValueError("user_id cannot be empty")

        if not device_id:
            raise ValueError("device_id cannot be empty")

        # Atomic DB Update
        # Ensures consistency under concurrency

        with transaction.atomic():
            updated_count = (
                UserDeviceToken.objects.filter(user_id=user_id, device_id=device_id, is_active=True)
                .exclude(id=token_id)
                .update(is_active=False)
            )

        logger.info(
            f"INFO:-----------> Deactivated {updated_count} previous sessions for user_id={user_id}, device_id={device_id}"
        )

        return updated_count

    except ValueError as exc:
        # Business logic error → no retry
        logger.error(f"ERROR:------->> Deactivate session task input error: {exc}")
        raise exc

    except ObjectDoesNotExist:
        # User/session truly missing → no retry
        logger.warning(f"WARNING:-----> User/session not found for user_id={user_id}, device_id={device_id}")
        return 0

    except Exception as exc:
        logger.exception(f"ERROR:------->> Deactivate session task error: {exc}")
        raise exc
