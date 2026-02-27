from typing import Any, Dict

from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView

from apps.vacancies.models import Vacancy
from apps.vacancies.selectors import VacancySelector


class VacancyDetailView(DetailView):
    template_name = "vacancies/vacancy_detail.html"
    context_object_name = "vacancy"
    pk_url_kwarg = "vacancy_pk"

    def get_queryset(self) -> QuerySet[Vacancy]:
        return VacancySelector().get_vacancies()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"name": _("Vacancies"), "url": reverse("vacancies:list")},
            {"name": self.object.title},
        ]
        return context
