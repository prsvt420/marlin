from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin

from apps.vacancies.models import ProfessionalArea


@admin.register(ProfessionalArea)
class ProfessionalAreaAdmin(TranslationAdmin):
    list_per_page = 25
    list_display = ("name",)
    search_fields = ("name",)
    search_help_text = _("Search by professional field name")
    ordering = ("name",)
