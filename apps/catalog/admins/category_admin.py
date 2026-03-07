from django.contrib import admin
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from apps.catalog.models import Category


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_per_page = 25
    prepopulated_fields = {
        "slug": ("name",),
    }
    list_display = (
        "name",
        "parent",
        "is_active",
        "image_preview",
        "sort_order",
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
        ("image", "image_preview"),
        ("created_at", "updated_at"),
    )
    search_help_text = _("Search by category name")
    list_select_related = ("parent",)

    @admin.display(description=_("Image preview"))
    def image_preview(self, obj: Category) -> str:
        return format_html(
            "<img src='{}' style='max-height: 100px;'/>",
            (
                obj.image.url
                if obj.image
                else static("catalog/img/default-category-image.webp")
            ),
        )
