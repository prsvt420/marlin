import django_filters
from django.db.models import Q, QuerySet
from django.utils.translation import gettext_lazy as _

from apps.vacancies.choices import WorkExperience, WorkSchedule
from apps.vacancies.models import Vacancy
from apps.vacancies.selectors import CitySelector, ProfessionalAreaSelector


class VacancyFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(
        method="filter_search",
        label=_("Search"),
    )
    work_experience = django_filters.MultipleChoiceFilter(
        choices=WorkExperience,
        label=_("Work experience"),
    )
    work_schedule = django_filters.MultipleChoiceFilter(
        choices=WorkSchedule,
        label=_("Work schedule"),
    )
    professional_area = django_filters.ModelMultipleChoiceFilter(
        queryset=ProfessionalAreaSelector().get_professional_areas(),
        label=_("Professional area"),
    )
    city = django_filters.ModelMultipleChoiceFilter(
        queryset=CitySelector().get_cities(),
        label=_("City"),
    )

    class Meta:
        model = Vacancy
        fields = ("work_experience", "work_schedule", "professional_area", "q")

    def filter_search(
        self, queryset: QuerySet[Vacancy], name: str, value: str
    ) -> QuerySet[Vacancy]:
        if not value:
            return queryset

        return queryset.filter(
            Q(title__icontains=value)
            | Q(description__icontains=value)
            | Q(short_description__icontains=value)
        )
