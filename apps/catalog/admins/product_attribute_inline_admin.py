from django.contrib import admin

from apps.catalog.models import ProductAttribute


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1
