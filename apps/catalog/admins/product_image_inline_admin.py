from unfold.admin import TabularInline

from apps.catalog.models import ProductImage


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1
    tab = True
