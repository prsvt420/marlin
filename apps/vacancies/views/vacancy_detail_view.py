from django.db.models import QuerySet
from django.views.generic import DetailView

from apps.vacancies.models import Vacancy
from apps.vacancies.repositories import VacancyRepository


class VacancyDetailView(DetailView):
    """View for displaying the vacancy detail."""

    model = Vacancy
    template_name = "vacancies/vacancy_detail.html"
    context_object_name = "vacancy"

    def get_queryset(self) -> QuerySet[Vacancy]:
        """Return all active vacancies."""
        return VacancyRepository().get_filtered()
