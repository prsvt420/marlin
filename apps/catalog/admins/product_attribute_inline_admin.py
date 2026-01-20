from django.contrib import admin

from apps.catalog.models import ProductAttribute


class ProductAttributeInline(admin.TabularInline):
    """Configuration for inline administration of the ProductAttribute model."""  # noqa: E501

    model = ProductAttribute
    extra = 1
