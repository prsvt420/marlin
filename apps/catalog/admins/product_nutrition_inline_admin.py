from django.contrib import admin

from apps.catalog.models import ProductNutrition


class ProductNutritionInline(admin.StackedInline):
    """Configuration for inline administration of the ProductNutrition model."""  # noqa: E501

    model = ProductNutrition
    extra = 0
    max_num = 1
