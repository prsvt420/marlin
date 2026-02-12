from typing import Any, Dict, Optional

from django.db.models import QuerySet
from django.views.generic import ListView

from apps.vacancies.models import Vacancy
from apps.vacancies.selectors import VacancySelector


class VacancyListView(ListView):
    template_name = "vacancies/vacancy_list.html"
    context_object_name = "vacancies"
    paginate_by = 12
    paginate_orphans = 4

    @property
    def search_query(self) -> Optional[str]:
        search_query: Optional[str] = self.request.GET.get(key="q")
        return search_query.strip() if search_query else None

    def get_queryset(self) -> QuerySet[Vacancy]:
        search_query: Optional[str] = self.search_query
        return VacancySelector().get_vacancies(search_query=search_query)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["search_query"] = self.search_query
        return context
