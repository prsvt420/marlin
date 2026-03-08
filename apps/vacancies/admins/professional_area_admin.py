from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TabbedTranslationAdmin

from apps.core.admins import BaseModelAdmin
from apps.vacancies.models import ProfessionalArea


@admin.register(ProfessionalArea)
class ProfessionalAreaAdmin(BaseModelAdmin, TabbedTranslationAdmin):
    search_fields = ("name",)
    search_help_text = _("Search by professional field name")
