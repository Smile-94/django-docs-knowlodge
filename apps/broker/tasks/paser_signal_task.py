import logging

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.db.transaction import atomic

from _library.functions.number_utils import round_half_up
from apps.broker.functions.signal_parser import parse_signal
from apps.broker.models.choices import SignalStatusChoices
from apps.broker.models.signals_model import TradingSignal
from apps.order.models.choices import Action, OrderStatus
from apps.order.models.order_model import Order, OrderHistory
from apps.order.tasks.order_life_cycle_task import broadcast_order_event, simulate_order_lifecycle

logger = logging.getLogger(__name__)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def process_signal_task(self, signal_id):
    signal = TradingSignal.objects.get(id=signal_id)
    signal.status = SignalStatusChoices.PROCESSING.value
    signal.save(update_fields=["status"])

    try:
        parsed = parse_signal(signal.raw_message)

        if not parsed["valid"]:
            signal.status = SignalStatusChoices.FAILED.value
            signal.error_message = parsed["error"]
            signal.save(update_fields=["status", "error_message"])
            data = {
                "event": "signal.invalid",
                "trading_id": signal.id,
                "user": signal.user.username,
                "account_id": signal.account_id,
                "error_message": signal.error_message,
            }
            notify_signal_invalid.delay(data)
            return

        data = parsed["data"]
        with atomic():
            order = Order.objects.create(
                user=signal.user,
                signal=signal,
                instrument=data["instrument"],
                entry_price=round_half_up(data["price"], 4),
                stop_loss=round_half_up(data["stop_loss"], 4),
                take_profit=round_half_up(data["take_profit"], 4),
                status=OrderStatus.PENDING.value,
            )
            if data["action"] == "BUY":
                order.action = Action.BUY.value
            if data["action"] == "SELL":
                order.action = Action.SELL.value
            order.save()
            data = {
                "type": f"order.{OrderStatus.PENDING.value}",
                "order_id": order.order_id,
                "instrument": order.instrument,
                "entry_price": float(order.entry_price),
                "status": order.status,
            }
            broadcast_order_event.delay(data)

            simulate_order_lifecycle.delay(order.id)

            logger.info(f"INFO: ------------>> Created order: {order.order_id}")

            order_history = OrderHistory.objects.create(
                order=order,
                status=OrderStatus.PENDING.value,
                description={"message": "Order pending"},
            )
            order_history.save()
            logger.info(f"INFO: ------------>> Created order history: {order_history.id}")

        signal.status = SignalStatusChoices.SUCCESS.value
        signal.save()

    except Exception as e:
        signal.status = SignalStatusChoices.FAILED.value
        signal.error_message = str(e)
        signal.save(update_fields=["status", "error_message"])
        raise


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def notify_signal_invalid(self, data):
    try:
        channel_layer = get_channel_layer()

        group_name = "signal_invalid"
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "signal_invalid_event",  # must match consumer method
                "data": data,
            },
        )

    except Exception as exc:
        logger.exception(f"ERROR:---------->> Notify signal invalid task error: {exc}")
        raise exc
