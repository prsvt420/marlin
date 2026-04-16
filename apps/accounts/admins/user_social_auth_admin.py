from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.accounts.models import ProxyUserSocialAuth
from apps.core.admins import BaseModelAdmin


@admin.register(ProxyUserSocialAuth)
class UserSocialAuthAdmin(BaseModelAdmin, ModelAdmin):
    list_display = ("user", "provider", "uid", "created", "modified")
    list_filter = ("provider",)
    autocomplete_fields = ("user",)
    readonly_fields = ("created", "modified")
    list_select_related = True
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "uid",
    )
