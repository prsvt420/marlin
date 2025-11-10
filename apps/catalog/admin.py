from decimal import Decimal

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    Attribute,
    Category,
    Product,
    ProductAttribute,
    ProductImage,
    ProductNutrition,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""

    list_per_page = 25
    prepopulated_fields = {
        "slug": ("name",),
    }
    list_display = ("name", "parent", "is_active", "sort_order")
    list_editable = ("is_active", "sort_order")
    list_filter = ("name", "is_active")
    search_fields = (
        "sort_order",
        "name",
    )
    ordering = ("parent__name", "sort_order")
    empty_value_display = "—"
    readonly_fields = ("created_at", "updated_at")
    fields = (
        ("name", "slug"),
        "parent",
        "description",
        "sort_order",
        "is_active",
        ("created_at", "updated_at"),
    )
    search_help_text = _("Search by category name")
    list_select_related = ("parent",)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    """Admin configuration for Attribute model."""

    list_per_page = 25
    list_display = ("name",)
    search_fields = ("name",)
    search_help_text = _("Search by attribute name")
    ordering = ("name",)


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    """Admin configuration for ProductAttribute model."""

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
class ProductImageAdmin(admin.ModelAdmin):
    """Admin configuration for ProductImage model."""

    list_per_page = 25
    list_display = ("product", "image_path", "sort_order")
    list_editable = ("sort_order",)
    search_fields = ("product__name",)
    ordering = ("product__name", "sort_order")
    search_help_text = _("Search by product name")


@admin.register(ProductNutrition)
class ProductNutritionAdmin(admin.ModelAdmin):
    """Admin configuration for ProductNutrition model."""

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
    """Inline for product images."""

    model = ProductImage
    extra = 1


class ProductNutritionInline(admin.StackedInline):
    """Inline for product attributes."""

    model = ProductNutrition
    extra = 0
    max_num = 1


class ProductAttributeInline(admin.TabularInline):
    """Inline for product nutritional information."""

    model = ProductAttribute
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for Product model."""

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
        """Return price with discount applied.

        Returns:
            Decimal: Final price.
        """
        return obj.get_final_price()
