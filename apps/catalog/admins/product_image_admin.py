from django.contrib import admin
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from apps.catalog.models import ProductImage
from apps.core.admins import BaseModelAdmin


@admin.register(ProductImage)
class ProductImageAdmin(BaseModelAdmin):
    list_display = ("product", "image_preview", "sort_order")
    search_fields = ("product__name",)
    search_help_text = _("Search by product name")

    @admin.display(description=_("Image preview"))
    def image_preview(self, obj: ProductImage) -> str:
        return format_html(
            "<img src='{}' style='max-height: 100px;'/>",
            (
                obj.image.url
                if obj.image
                else static("catalog/img/default-product-image.webp")
            ),
        )
