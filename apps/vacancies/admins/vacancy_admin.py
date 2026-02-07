from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise
from modeltranslation.admin import TranslationAdmin

from apps.vacancies.models import Vacancy


@admin.register(Vacancy)
class VacancyAdmin(TranslationAdmin):

    list_per_page = 25
    list_display = ("title", "city", "formatted_salary", "is_active")
    list_display_links = ("title",)
    list_editable = ("is_active",)
    search_fields = (
        "title",
        "short_description",
        "description",
    )
    search_help_text = _("Search by vacancy title and description")
    list_filter = (
        "professional_area__name",
        "is_active",
        "experience_level",
        "work_schedule",
        "city",
    )
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    fields = (
        ("title",),
        "short_description",
        "description",
        "professional_area",
        "city",
        "salary_from",
        "salary_to",
        "experience_level",
        "work_schedule",
        "is_active",
        ("created_at", "updated_at"),
    )
    list_select_related = (
        "city",
        "city__region",
        "professional_area",
    )
    empty_value_display = "—"

    @admin.display(description=_("Salary"), ordering="salary_from")
    def formatted_salary(self, obj: Vacancy) -> StrOrPromise:
        return obj.formatted_salary
