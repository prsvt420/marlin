from django.db.models import QuerySet

from apps.vacancies.models import Vacancy


class VacancySelector:

    def get_vacancies(
        self,
        *,
        only_active: bool = True,
    ) -> QuerySet[Vacancy]:
        vacancies: QuerySet[Vacancy] = Vacancy.objects.select_related(
            "city",
            "city__region",
            "professional_area",
        )

        if only_active:
            vacancies = vacancies.filter(is_active=True)

        return vacancies
