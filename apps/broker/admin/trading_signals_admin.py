from django.contrib import admin
from rangefilter.filters import DateTimeRangeFilterBuilder

from apps.broker.models import TradingSignal


# <<--------------------------------- Trading Signal Admin --------------------------------->>
@admin.register(TradingSignal)
class TradingSignalAdmin(admin.ModelAdmin):
    list_display = ("id", "user__id", "user", "account", "status", "created_at", "updated_at")
    list_filter = (
        "active_status",
        ("created_at", DateTimeRangeFilterBuilder()),
        ("updated_at", DateTimeRangeFilterBuilder()),
    )
    search_fields = ("user__username",)
    ordering = ("-id",)
    list_per_page = 20
