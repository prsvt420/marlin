from typing import Optional

from django.db.models import Q, QuerySet

from apps.vacancies.models import Vacancy


class VacancySelector:

    def get_vacancies(
        self,
        *,
        search_query: Optional[str] = None,
        only_active: bool = True,
    ) -> QuerySet[Vacancy]:
        vacancies: QuerySet[Vacancy] = Vacancy.objects.select_related(
            "city",
            "city__region",
            "professional_area",
        )

        if only_active:
            vacancies = vacancies.filter(is_active=True)

        if search_query:
            vacancies = vacancies.filter(
                Q(title__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(short_description__icontains=search_query)
            )

        return vacancies
