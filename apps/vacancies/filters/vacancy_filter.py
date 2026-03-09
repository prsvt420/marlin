import django_filters
from django.contrib.postgres import search
from django.db.models import QuerySet
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

        search_vector: search.SearchVector = search.SearchVector(
            "title", "description", "short_description"
        )
        search_query: search.SearchQuery = search.SearchQuery(value=value)

        return (
            queryset.annotate(
                search=search_vector,
                rank=search.SearchRank(
                    search_vector, search_query, cover_density=True
                ),
            )
            .filter(search=search_query)
            .order_by("-rank")
        )
