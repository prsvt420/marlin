from django.contrib import admin

from apps.catalog.models import ProductImage


class ProductImageInline(admin.TabularInline):
    """Configuration for inline administration of the ProductImage model."""

    model = ProductImage
    extra = 1
