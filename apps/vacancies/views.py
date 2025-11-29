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
    """

    model = Vacancy
    template_name = "vacancies/vacancy_list.html"
    context_object_name = "vacancies"
    paginate_by = 12
    paginate_orphans = 4

    def get_queryset(self) -> QuerySet[Vacancy]:
        """Return the queryset of vacancies.

        Returns:
            QuerySet[Vacancy]: A queryset of Vacancy objects.
        """
        search_query: str = self.search_query

        return VacancyRepository.filter(search_query=search_query)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add additional context variables to the template.

        Args:
            **kwargs: Additional context passed to the base implementation.

        Returns:
            Dict[str, Any]: The context dictionary for the template.
        """
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["search_query"] = self.search_query
        return context

    @property
    def search_query(self) -> str:
        """Return the search query string from the request.

        Fetches the 'q' GET parameter and strips whitespace from
        the beginning and end.

        Returns:
            str: The cleaned search query string. Returns an empty
            string if no query parameter is provided.
        """
        return self.request.GET.get("q", "").strip()


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
        return VacancyRepository.filter()
