from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.contrib.filters.admin import RelatedDropdownFilter

from apps.core.admins import BaseModelAdmin
from apps.vacancies.models import City


@admin.register(City)
class CityAdmin(BaseModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "name",
        "region",
    )
    readonly_fields = ("created_at", "updated_at")
    list_filter = (("region", RelatedDropdownFilter),)
    list_select_related = ("region",)
    search_fields = ("name", "region__name")
    search_help_text = _("Search by city and region name")
