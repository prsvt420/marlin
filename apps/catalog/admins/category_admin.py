from django.contrib import admin
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.contrib.filters.admin import RelatedDropdownFilter

from apps.catalog.models import Category
from apps.core.admins import BaseModelAdmin


@admin.register(Category)
class CategoryAdmin(BaseModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "name",
        "parent",
        "is_active",
        "image_preview",
        "sort_order",
    )
    readonly_fields = ("created_at", "updated_at")
    prepopulated_fields = {
        "slug": ("name",),
    }
    autocomplete_fields = ("parent",)
    list_filter = ("is_active", ("parent", RelatedDropdownFilter))
    list_select_related = ("parent",)
    search_fields = ("name",)
    search_help_text = _("Search by category name")

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
