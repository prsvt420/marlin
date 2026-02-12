from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from apps.catalog.models import ProductAttribute


@admin.register(ProductAttribute)
class ProductAttributeAdmin(TranslationAdmin):
    list_per_page = 25
    list_display = (
        "product",
        "attribute",
        "value",
    )
    list_filter = ("attribute", "product__category")
    search_fields = ("product__name",)
    ordering = ("product__name",)
    search_help_text = _("Search by product name")
    list_editable = ("value",)
