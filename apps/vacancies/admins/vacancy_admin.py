from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.contrib.filters.admin import (
    ChoicesDropdownFilter,
    RelatedDropdownFilter,
)

from apps.core.admins import BaseModelAdmin
from apps.vacancies.models import Vacancy


@admin.register(Vacancy)
class VacancyAdmin(BaseModelAdmin, TabbedTranslationAdmin):
    list_display = (
        "title",
        "city",
        "professional_area",
        "formatted_salary",
        "is_active",
    )
    readonly_fields = ("created_at", "updated_at")
    list_filter = (
        "is_active",
        ("work_experience", ChoicesDropdownFilter),
        ("work_schedule", ChoicesDropdownFilter),
        ("professional_area", RelatedDropdownFilter),
        ("city", RelatedDropdownFilter),
    )
    list_select_related = (
        "city",
        "city__region",
        "professional_area",
    )
    search_fields = (
        "title",
        "short_description",
        "description",
    )
    search_help_text = _("Search by vacancy title and description")

    @admin.display(description=_("Salary"), ordering="salary_from")
    def formatted_salary(self, obj: Vacancy) -> StrOrPromise:
        return obj.formatted_salary
