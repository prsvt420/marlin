from django.db.models import Prefetch, QuerySet
from django.shortcuts import get_object_or_404

from apps.catalog.models import Category


class CategoryRepository:
    """Repository for Category model database operations."""

    @staticmethod
    def get_by_slug(slug: str) -> Category:
        """Return a single active category by its slug.

        Args:
            slug (str): The slug of the category to retrieve.

        Returns:
            Category: The active Category object matching the given slug.

        Raises:
            Http404: If no active category with the given slug is found.
        """
        return get_object_or_404(Category, slug=slug, is_active=True)

    @staticmethod
    def get_parents() -> QuerySet[Category]:
        """Return a queryset of all active parent categories.

        Returns:
            QuerySet[Category]: A queryset containing all active parent
            Category objects with their active subcategories prefetched.
        """
        return Category.objects.filter(
            parent__isnull=True, is_active=True
        ).prefetch_related(
            Prefetch(
                "subcategories",
                queryset=Category.objects.filter(is_active=True),
            )
        )
