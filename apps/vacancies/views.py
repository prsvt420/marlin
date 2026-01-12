from typing import Any, Dict

from django.db.models import QuerySet
from django.views import generic
from django.views.generic import ListView

from apps.vacancies.models import Vacancy
from apps.vacancies.repositories.vacancy_repository import VacancyRepository


class VacancyListView(ListView):
    """View for displaying the vacancy list."""

    model = Vacancy
    template_name = "vacancies/vacancy_list.html"
    context_object_name = "vacancies"
    paginate_by = 12
    paginate_orphans = 4

    def get_queryset(self) -> QuerySet[Vacancy]:
        """Return filtered vacancies."""
        search_query: str = self.search_query

        return VacancyRepository.filter(search_query=search_query)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add additional context variables to the template."""
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["search_query"] = self.search_query
        return context

    @property
    def search_query(self) -> str:
        """Return the current search query from GET parameters."""
        return self.request.GET.get("q", "").strip()


class VacancyDetailView(generic.DetailView):
    """View for displaying the vacancy detail."""

    model = Vacancy
    template_name = "vacancies/vacancy_detail.html"
    context_object_name = "vacancy"

    def get_queryset(self) -> QuerySet[Vacancy]:
        """Return all active vacancies."""
        return VacancyRepository.filter()
