from django.db.models import QuerySet
from django.views.generic import DetailView

from apps.vacancies.models import Vacancy
from apps.vacancies.selectors import VacancySelector


class VacancyDetailView(DetailView):
    template_name = "vacancies/vacancy_detail.html"
    context_object_name = "vacancy"
    pk_url_kwarg = "vacancy_pk"

    def get_queryset(self) -> QuerySet[Vacancy]:
        return VacancySelector().get_vacancies()
