from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from apps.catalog.admins import (
    ProductImageInline,
    ProductNutritionInline,
)
from apps.catalog.models import Product


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_per_page = 25
    prepopulated_fields = {
        "slug": ("name",),
    }
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
    list_display_links = ("name",)
    list_editable = ("is_active", "discount", "stock")
    search_fields = ("name",)
    search_help_text = _("Search by product name")
    list_filter = ("category__name", "is_active", "unit_type")
    date_hierarchy = "created_at"
    readonly_fields = (
        "created_at",
        "updated_at",
        "final_price",
        "is_available",
    )
    inlines = (
        ProductImageInline,
        ProductNutritionInline,
    )
    fields = (
        ("name", "slug"),
        "description",
        "composition",
        "attributes",
        "unit_type",
        "price",
        "discount",
        "final_price",
        "category",
        "stock",
        "is_active",
        "is_available",
        ("created_at", "updated_at"),
    )
    autocomplete_fields = ("category",)
