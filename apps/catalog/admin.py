from decimal import Decimal

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise
from modeltranslation.admin import TranslationAdmin

from .models import (
    Attribute,
    Category,
    Product,
    ProductAttribute,
    ProductImage,
    ProductNutrition,
)


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    """Configuration for administration of the Category model."""

    list_per_page = 25
    prepopulated_fields = {
        "slug": ("name",),
    }
    list_display = (
        "name",
        "parent",
        "is_active",
        "sort_order",
        "image_preview",
    )
    list_editable = ("is_active", "sort_order")
    list_filter = ("parent", "is_active")
    autocomplete_fields = ("parent",)
    search_fields = (
        "sort_order",
        "name",
    )
    ordering = ("parent__name", "sort_order")
    empty_value_display = "—"
    readonly_fields = ("created_at", "updated_at", "image_preview")
    fields = (
        ("name", "slug"),
        "parent",
        "description",
        "sort_order",
        "is_active",
        ("image_path", "image_preview"),
        "alt_text",
        ("created_at", "updated_at"),
    )
    search_help_text = _("Search by category name")
    list_select_related = ("parent",)

    @admin.display(description=_("Image preview"))
    def image_preview(self, obj: Category) -> StrOrPromise:
        """Return an HTML image preview for the category."""
        if obj.image_path:
            return format_html(
                "<img src='{}' alt='{}' style='max-height: 100px;'/>",
                obj.image_path.url,
                obj.alt_text or "",
            )
        return _("No image available")


@admin.register(Attribute)
class AttributeAdmin(TranslationAdmin):
    """Configuration for administration of the Attribute model."""

    list_per_page = 25
    list_display = ("name",)
    search_fields = ("name",)
    search_help_text = _("Search by attribute name")
    ordering = ("name",)


@admin.register(ProductAttribute)
class ProductAttributeAdmin(TranslationAdmin):
    """Configuration for administration of the ProductAttribute model."""

    list_per_page = 25
    list_display = (
        "product",
        "attribute",
        "value",
    )
    list_filter = ("attribute", "product__category")
    search_fields = ("product__name",)
    ordering = ("product__name",)
    search_help_text = _("Search by product name")
    list_editable = ("value",)


@admin.register(ProductImage)
class ProductImageAdmin(TranslationAdmin):
    """Configuration for administration of the ProductImage model."""

    list_per_page = 25
    list_display = ("product", "image_path", "sort_order")
    list_editable = ("sort_order",)
    search_fields = ("product__name",)
    ordering = ("product__name", "sort_order")
    search_help_text = _("Search by product name")


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


class ProductImageInline(admin.TabularInline):
    """Configuration for inline administration of the ProductImage model."""

    model = ProductImage
    extra = 1


class ProductNutritionInline(admin.StackedInline):
    """Configuration for inline administration of the ProductNutrition model."""  # noqa: E501

    model = ProductNutrition
    extra = 0
    max_num = 1


class ProductAttributeInline(admin.TabularInline):
    """Configuration for inline administration of the ProductAttribute model."""  # noqa: E501

    model = ProductAttribute
    extra = 1


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    """Configuration for administration of the Product model."""

    list_per_page = 25
    prepopulated_fields = {
        "slug": ("name",),
    }
    list_display = (
        "sku",
        "name",
        "category",
        "price",
        "discount",
        "final_price",
        "stock",
        "is_active",
    )
    list_display_links = ("name",)
    list_editable = ("is_active", "discount", "stock")
    search_fields = (
        "sku",
        "name",
    )
    search_help_text = _("Search by name or article (SKU)")
    list_filter = ("category__name", "is_active", "unit_type")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    inlines = (
        ProductImageInline,
        ProductNutritionInline,
        ProductAttributeInline,
    )
    fields = (
        ("name", "slug"),
        "description",
        "composition",
        "unit_type",
        "price",
        "discount",
        "category",
        "sku",
        "stock",
        "is_active",
        ("created_at", "updated_at"),
    )
    autocomplete_fields = ("category",)

    @admin.display(description=_("Final price"))
    def final_price(self, obj: Product) -> Decimal:
        """Return the price with discount applied."""
        return obj.get_final_price()
