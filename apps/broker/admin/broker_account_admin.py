from django.contrib import admin
from rangefilter.filters import DateTimeRangeFilterBuilder

from apps.broker.models import BrokerAccount


# <<--------------------------------- Broker Account Admin --------------------------------->>
@admin.register(BrokerAccount)
class BrokerAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "user__id", "user", "account_id", "account_name", "active_status", "created_at", "updated_at")
    list_filter = (
        "active_status",
        ("created_at", DateTimeRangeFilterBuilder()),
        ("updated_at", DateTimeRangeFilterBuilder()),
    )
    search_fields = ("user__id", "user__username", "account_id")
    ordering = ("-id",)
    list_per_page = 20
