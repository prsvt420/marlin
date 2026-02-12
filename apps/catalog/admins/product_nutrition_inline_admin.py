from django.contrib import admin

from apps.catalog.models import ProductNutrition


class ProductNutritionInline(admin.StackedInline):
    model = ProductNutrition
    extra = 0
    max_num = 1
