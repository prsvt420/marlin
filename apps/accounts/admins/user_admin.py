from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)

from apps.accounts.models import User
from apps.core.admins import BaseModelAdmin


@admin.register(User)
class UserAdmin(_UserAdmin, BaseModelAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = (
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "middle_name",
                    "email",
                    "phone_number",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )
    readonly_fields = ("email", "last_login", "date_joined")
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
    search_help_text = _(
        "Search by first name, last name, middle name, email and phone number"
    )
    ordering = ("email",)
