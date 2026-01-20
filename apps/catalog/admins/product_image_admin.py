from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from apps.catalog.models import ProductImage


@admin.register(ProductImage)
class ProductImageAdmin(TranslationAdmin):
    """Configuration for administration of the ProductImage model."""

    list_per_page = 25
    list_display = ("product", "image_path", "sort_order")
    list_editable = ("sort_order",)
    search_fields = ("product__name",)
    ordering = ("product__name", "sort_order")
    search_help_text = _("Search by product name")
