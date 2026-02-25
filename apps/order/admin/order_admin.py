from django.contrib import admin
from rangefilter.filters import DateTimeRangeFilterBuilder

from apps.order.models.order_model import Order, OrderHistory


# <<--------------------------------- Order Admin --------------------------------->>
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user__id",
        "user",
        "order_id",
        "action",
        "instrument",
        "entry_price",
        "stop_loss",
        "take_profit",
        "status",
    )
    list_filter = (
        "active_status",
        ("created_at", DateTimeRangeFilterBuilder()),
        ("updated_at", DateTimeRangeFilterBuilder()),
    )
    search_fields = ("user__username", "order_id")
    ordering = ("-id",)
    list_per_page = 20


# <<--------------------------------- Order History Admin --------------------------------->>
@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "status", "created_at", "updated_at")
    list_filter = (
        "active_status",
        ("created_at", DateTimeRangeFilterBuilder()),
        ("updated_at", DateTimeRangeFilterBuilder()),
    )
    search_fields = ("order__user__username", "order__order_id")
    ordering = ("-id",)
    list_per_page = 20
