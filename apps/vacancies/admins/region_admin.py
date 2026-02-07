from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from apps.vacancies.models import Region


@admin.register(Region)
class RegionAdmin(TranslationAdmin):

    list_per_page = 25
    list_display = ("name",)
    search_fields = ("name",)
    search_help_text = _("Search by region name")
    ordering = ("name",)
