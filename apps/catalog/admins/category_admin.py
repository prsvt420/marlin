from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise
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

        if obj.image_path:
            return format_html(
                "<img src='{}' alt='{}' style='max-height: 100px;'/>",
                obj.image_path.url,
                obj.alt_text or "",
            )
        return _("No image available")
