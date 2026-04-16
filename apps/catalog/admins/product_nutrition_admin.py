from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.catalog.models import ProductNutrition
from apps.core.admins import BaseModelAdmin


@admin.register(ProductNutrition)
class ProductNutritionAdmin(BaseModelAdmin):
    list_display = (
        "product",
        "calories",
        "proteins",
        "fats",
        "carbs",
    )
    search_fields = ("product__name",)
    search_help_text = _("Search by product name")
    autocomplete_fields = ("product",)
