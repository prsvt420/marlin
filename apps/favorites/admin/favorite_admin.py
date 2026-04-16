from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.core.admins import BaseModelAdmin
from apps.favorites.models import Favorite


@admin.register(Favorite)
class FavoriteAdmin(BaseModelAdmin):
    list_display = (
        "user",
        "product",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    search_fields = (
        "user__email",
        "product__name",
    )
    search_help_text = _("Search by email or product name")
    autocomplete_fields = (
        "user",
        "product",
    )
