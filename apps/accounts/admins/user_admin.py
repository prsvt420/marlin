from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User


@admin.register(User)
class UserAdmin(_UserAdmin):

    list_per_page = 25
    list_display = (
        "username",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    list_editable = ("is_active",)
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
    )
    search_fields = (
        "first_name",
        "last_name",
        "middle_name",
        "email",
        "phone_number",
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "middle_name",
                    "email",
                    "phone_number",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    ordering = ("first_name", "last_name", "middle_name", "email")
    empty_value_display = "—"
    readonly_fields = ("last_login",)
    search_help_text = _(
        "Search by first name, last name, middle name, email and phone number"
    )

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
