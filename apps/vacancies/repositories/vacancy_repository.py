from typing import Optional

from django.db.models import Q, QuerySet

from apps.vacancies.models import Vacancy


class VacancyRepository:
    """Repository for Vacancy model database operations."""

    @staticmethod
    def all() -> QuerySet[Vacancy]:
        """Return a queryset of all vacancies with related data preloaded.

        Returns:
            QuerySet[Vacancy]: A queryset containing all Vacancy objects
            with related data preloaded.
        """
        return Vacancy.objects.all().select_related("city")

    @staticmethod
    def filter(
        *,
        search_query: Optional[str] = None,
        only_active: bool = True,
    ) -> QuerySet[Vacancy]:
        """Return a filtered queryset of vacancies.

        Args:
            search_query (Optional[str]): The query to search.
            only_active (bool): If True, returns only active products.
            Default True.

        Returns:
            QuerySet[Vacancy]: A queryset containing active Vacancy
            objects filtered according to the provided criteria.
        """
        queryset: QuerySet[Vacancy] = VacancyRepository.all()

        if only_active:
            queryset = queryset.filter(is_active=True)

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
                | Q(description__icontains=search_query)  # noqa: W503
                | Q(short_description__icontains=search_query)  # noqa: W503
            )

        return queryset
