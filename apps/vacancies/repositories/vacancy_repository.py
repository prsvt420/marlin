from django.db.models import Q, QuerySet

from apps.vacancies.models import Vacancy


class VacancyRepository:
    """Repository for Vacancy model database operations."""

    @staticmethod
    def find_active() -> QuerySet[Vacancy]:
        """Return a queryset of vacancies marked as active.

        Only vacancies with `is_active=True` are included in the queryset.

        Returns:
            QuerySet[Vacancy]: A queryset containing active Vacancy objects.
        """
        return Vacancy.objects.filter(is_active=True).select_related("city")

    @staticmethod
    def find_by_search_query(search_query: str) -> QuerySet[Vacancy]:
        """Return a queryset of active vacancies filtered by search query.

        Search is performed in fields: title, description
        and short_description.

        Args:
            search_query (str): The query to search.

        Returns:
            QuerySet[Vacancy]: A queryset containing active Vacancy objects
            filtered by the search term.
        """
        return VacancyRepository.find_active().filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)  # noqa: W503
            | Q(short_description__icontains=search_query)  # noqa: W503
        )
