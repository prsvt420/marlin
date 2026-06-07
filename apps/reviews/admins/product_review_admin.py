from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.core.admins import BaseModelAdmin
from apps.reviews.models import ProductReview


@admin.register(ProductReview)
class ProductReviewAdmin(BaseModelAdmin):
    list_display = (
        "user",
        "product",
        "rating",
        "created_at",
        "updated_at",
    )
    list_editable = ("rating",)
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
    list_filter = ("rating",)
    list_select_related = ("user", "product")
    date_hierarchy = "created_at"
