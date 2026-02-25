from django.core.validators import MinValueValidator
from django.db import models

from apps.broker.models.signals_model import TradingSignal
from apps.common.functions.unique_id_generator import generate_custom_id
from apps.common.models import BaseModel, TimeStampedModel, UserStampModel
from apps.order.models.choices import Action, OrderStatus
from apps.user.models.user_model import User


class Order(BaseModel, TimeStampedModel):
    """Trading order"""

    order_id = models.CharField(max_length=50, unique=True, editable=False, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    signal = models.OneToOneField(TradingSignal, on_delete=models.SET_NULL, blank=True, null=True, related_name="signal_order")
    action = models.CharField(max_length=4, choices=Action.choices, blank=True, null=True)
    instrument = models.CharField(max_length=20)
    entry_price = models.DecimalField(max_digits=19, decimal_places=4, null=True, blank=True)
    stop_loss = models.DecimalField(max_digits=19, decimal_places=4, validators=[MinValueValidator(0)])
    take_profit = models.DecimalField(max_digits=19, decimal_places=4, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    class Meta:
        app_label = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        db_table = "order"
        ordering = ["-id"]
        indexes = [
            models.Index(fields=["user", "active_status"]),
        ]

    def clean(self):
        if not self.order_id:
            self.order_id = generate_custom_id(id_prefix="INV", field="order_id", model_class=self.__class__)
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_id}"

    def __repr__(self):
        return f"<Order: {self.order_id}>"


class OrderHistory(BaseModel, TimeStampedModel, UserStampModel):
    """Track order status changes"""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="history")
    status = models.CharField(max_length=20, choices=OrderStatus.choices)
    details = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["id"]
        indexes = [
            models.Index(fields=["order"]),
        ]

    def __str__(self):
        return f"{self.order.order_id} - {self.status}"

    def __repr__(self):
        return f"<Order History: {self.order.order_id} - {self.status}>"
