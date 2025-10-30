from django.contrib import admin

from .models import (
    City,
    ProfessionalArea,
    Region,
    Vacancy,
)


@admin.register(ProfessionalArea)
class ProfessionalAreaAdmin(admin.ModelAdmin):
    """Admin configuration for ProfessionalArea model."""

    list_per_page = 25
    list_display = ("name",)
    search_fields = ("name",)
    search_help_text = "Поиск по названию профессиональной области"
    ordering = ("name",)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    """Admin configuration for Region model."""

    list_per_page = 25
    list_display = ("name",)
    search_fields = ("name",)
    search_help_text = "Поиск по названию региона"
    ordering = ("name",)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """Admin configuration for City model."""

    list_per_page = 25
    list_display = (
        "name",
        "region",
    )
    list_filter = ("region__name",)
    search_fields = ("name", "region__name")
    ordering = ("name",)
    search_help_text = "Поиск по названию города и региона"
    list_select_related = ("region",)
    empty_value_display = "—"


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    """Admin configuration for Vacancy model."""

    list_per_page = 25
    list_display = ("title", "city", "formatted_salary", "is_active")
    list_display_links = ("title",)
    list_editable = ("is_active",)
    search_fields = (
        "title",
        "short_description",
        "description",
    )
    search_help_text = "Поиск по заголовку и описанию вакансии"
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

    @admin.display(description="Зарплата", ordering="salary_from")
    def formatted_salary(self, obj: Vacancy) -> str:
        """Return formatted salary.

        Returns:
            str: Formatted salary.
        """
        return obj.get_formatted_salary()
