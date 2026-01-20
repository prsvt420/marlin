from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.catalog.models import ProductNutrition


@admin.register(ProductNutrition)
class ProductNutritionAdmin(admin.ModelAdmin):
    """Configuration for administration of the ProductNutrition model."""

    list_per_page = 25
    list_display = (
        "product",
        "calories",
        "proteins",
        "fats",
        "carbs",
    )
    search_fields = ("product__name",)
    ordering = ("product__name",)
    search_help_text = _("Search by product name")
