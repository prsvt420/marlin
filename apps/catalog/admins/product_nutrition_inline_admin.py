from unfold.admin import TabularInline

from apps.catalog.models import ProductNutrition


class ProductNutritionInline(TabularInline):
    model = ProductNutrition
    extra = 0
    max_num = 1
    tab = True
    autocomplete_fields = ("product",)
