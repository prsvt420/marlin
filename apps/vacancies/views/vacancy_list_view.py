from django.db.models import QuerySet
from django_filters.views import FilterView

from apps.vacancies.filters import VacancyFilter
from apps.vacancies.models import Vacancy
from apps.vacancies.selectors import VacancySelector


class VacancyListView(FilterView):
    template_name = "vacancies/vacancy_list.html"
    context_object_name = "vacancies"
    paginate_by = 12
    paginate_orphans = 4
    filterset_class = VacancyFilter

    def get_queryset(self) -> QuerySet[Vacancy]:
        return VacancySelector().get_vacancies()
