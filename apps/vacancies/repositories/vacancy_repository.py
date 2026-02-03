from typing import Optional

from django.db.models import Q, QuerySet

from apps.vacancies.models import Vacancy


class VacancyRepository:
    """Repository for accessing Vacancy model."""

    def get_all(self) -> QuerySet[Vacancy]:
        """Return all vacancies with related prefetched."""
        return Vacancy.objects.all().select_related("city")

    def get_filtered(
        self,
        *,
        search_query: Optional[str] = None,
        only_active: bool = True,
    ) -> QuerySet[Vacancy]:
        """Return filtered vacancies."""
        queryset: QuerySet[Vacancy] = self.get_all()

        if only_active:
            queryset = queryset.filter(is_active=True)

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
                | Q(description__icontains=search_query)  # noqa: W503
                | Q(short_description__icontains=search_query)  # noqa: W503
            )

        return queryset
