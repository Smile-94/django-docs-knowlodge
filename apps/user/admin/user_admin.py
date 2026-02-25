from django.contrib import admin
from rangefilter.filters import DateTimeRangeFilterBuilder

from apps.user.models.user_model import User, UserDeviceToken, UserSession


# <<------------------------------------User Admin---------------------------------------->>
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_active", "is_staff", "is_superuser", "created_at", "updated_at")
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        ("created_at", DateTimeRangeFilterBuilder()),
        ("updated_at", DateTimeRangeFilterBuilder()),
    )
    search_fields = ("username", "email", "phone")
    ordering = ("-id",)
    list_per_page = 20


# <<------------------------------------User Session Admin---------------------------------------->>
@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user__id",
        "user",
        "device_id",
        "ip_address",
        "country",
        "city",
        "login_at",
        "last_activity",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "active_status",
        ("created_at", DateTimeRangeFilterBuilder()),
        ("updated_at", DateTimeRangeFilterBuilder()),
    )
    search_fields = ("user__username", "device_id", "ip_address", "country", "city")
    ordering = ("-id",)
    list_per_page = 20


# <<--------------------------- User Device Token ----------------------------->>
@admin.register(UserDeviceToken)
class UserDeviceTokenAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "device_id",
        "ip_address",
        "user_agent",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "is_active",
        ("created_at", DateTimeRangeFilterBuilder()),
        ("updated_at", DateTimeRangeFilterBuilder()),
    )
    search_fields = ("user__username", "device_id", "ip_address", "user_agent")
    ordering = ("-id",)
    list_per_page = 20
