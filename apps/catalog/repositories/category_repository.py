from django.db.models import Prefetch, QuerySet
from django.shortcuts import get_object_or_404

from apps.catalog.models import Category


class CategoryRepository:
    """Repository for accessing Category model."""

    @staticmethod
    def get_by_slug(slug: str) -> Category:
        """Retrieve a category by slug or raise 404 if not found."""
        return get_object_or_404(Category, slug=slug, is_active=True)

    @staticmethod
    def get_parents() -> QuerySet[Category]:
        """Return all active categories with parents."""
        return Category.objects.filter(
            parent__isnull=True, is_active=True
        ).prefetch_related(
            Prefetch(
                "subcategories",
                queryset=Category.objects.filter(is_active=True),
            )
        )
