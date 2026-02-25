from django.db import models

from apps.broker.models.broker_account_model import BrokerAccount
from apps.broker.models.choices import SignalStatusChoices
from apps.common.models import BaseModel, TimeStampedModel, UserStampModel
from apps.user.models.user_model import User


class TradingSignal(BaseModel, TimeStampedModel, UserStampModel):
    """Raw incoming trading signal"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="signals_user")
    account = models.ForeignKey(BrokerAccount, on_delete=models.CASCADE, related_name="signals_account", null=True, blank=True)
    raw_message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=SignalStatusChoices.choices, default=SignalStatusChoices.PENDING.value)
    error_message = models.TextField(null=True, blank=True)

    class Meta:
        app_label = "broker"
        verbose_name = "Trading Signal"
        verbose_name_plural = "Trading Signals"
        db_table = "broker_signal"
        ordering = ["-id"]
        indexes = [
            models.Index(fields=["user", "active_status"]),
        ]

    def __str__(self):
        return f"Signal from {self.user.username} at {self.created_at}"

    def __repr__(self):
        return f"<Signal: {self.user.username} - {self.created_at}>"
