from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.contrib.filters.admin import (
    ChoicesDropdownFilter,
    RelatedDropdownFilter,
)

from apps.catalog.admins import (
    ProductImageInline,
    ProductNutritionInline,
)
from apps.catalog.models import Product
from apps.core.admins import BaseModelAdmin


@admin.register(Product)
class ProductAdmin(BaseModelAdmin, TabbedTranslationAdmin):
    inlines = (
        ProductImageInline,
        ProductNutritionInline,
    )
    list_display = (
        "name",
        "category",
        "price",
        "discount",
        "final_price",
        "stock",
        "is_active",
        "is_available",
    )
    readonly_fields = (
        "final_price",
        "is_available",
        "created_at",
        "updated_at",
    )
    prepopulated_fields = {
        "slug": ("name",),
    }
    autocomplete_fields = ("category",)
    list_filter = (
        "is_active",
        ("unit_type", ChoicesDropdownFilter),
        ("category", RelatedDropdownFilter),
    )
    search_fields = ("name",)
    search_help_text = _("Search by product name")
