from typing import Any, Dict

from django.db.models import QuerySet
from django.views import generic
from django.views.generic import ListView

from apps.vacancies.models import Vacancy
from apps.vacancies.repositories.vacancy_repository import VacancyRepository


class VacancyListView(ListView):
    """Displays a list of vacancies.

    Uses the `vacancies/vacancy_list.html` template and provides
    a context variable `vacancies` containing all Vacancy objects.
    Optionally filtered by search query.
    """

    model = Vacancy
    template_name = "vacancies/vacancy_list.html"
    context_object_name = "vacancies"
    paginate_by = 12
    paginate_orphans = 4

    def get_queryset(self) -> QuerySet[Vacancy]:
        """Return the queryset of vacancies.

        If the `q` GET parameter is provided, the queryset is filtered
        based on the search query.

        Returns:
            QuerySet[Vacancy]: A queryset of Vacancy objects,
            optionally filtered by the search term.
        """
        search_query: str = self.request.GET.get("q", "").strip()

        if search_query:
            return VacancyRepository.find_by_search_query(
                search_query=search_query
            )

        return VacancyRepository.find_active()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add additional context variables to the template.

        Adds the current search query (if any) to the context
        under the key `search_query` to preserve the input in the search field.

        Args:
            **kwargs: Additional context passed to the base implementation.

        Returns:
            Dict[str, Any]: The context dictionary for the template.
        """
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        return context


class VacancyDetailView(generic.DetailView):
    """Displays detailed information about a specific vacancy.

    Uses the `vacancies/vacancy_detail.html` template and provides
    a context variable `vacancy` containing the selected Vacancy object.
    """

    model = Vacancy
    template_name = "vacancies/vacancy_detail.html"
    context_object_name = "vacancy"

    def get_queryset(self) -> QuerySet[Vacancy]:
        """Return the queryset of vacancies.

        Returns:
            QuerySet[Vacancy]: A queryset of Vacancy objects.
        """
        return VacancyRepository.find_active()
