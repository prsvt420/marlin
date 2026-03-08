from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TabbedTranslationAdmin

from apps.core.admins import BaseModelAdmin
from apps.vacancies.models import Region


@admin.register(Region)
class RegionAdmin(BaseModelAdmin, TabbedTranslationAdmin):
    search_fields = ("name",)
    search_help_text = _("Search by region name")
