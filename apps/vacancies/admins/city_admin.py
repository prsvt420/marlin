from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from apps.vacancies.models import City


@admin.register(City)
class CityAdmin(TranslationAdmin):
    """Configuration for administration of the City model."""

    list_per_page = 25
    list_display = (
        "name",
        "region",
    )
    list_filter = ("region__name",)
    search_fields = ("name", "region__name")
    ordering = ("name",)
    search_help_text = _("Search by city and region name")
    list_select_related = ("region",)
    empty_value_display = "—"
