from typing import List, Optional

from django.db.models import Prefetch, QuerySet

from apps.catalog.models import Category


class CategorySelector:

    def get_categories(
        self, *, only_active: bool = True
    ) -> QuerySet[Category]:
        categories: QuerySet[Category] = Category.objects.all()

        if only_active:
            categories = categories.filter(is_active=True)

        return categories

    def get_parent_categories(
        self, *, only_active: bool = True
    ) -> QuerySet[Category]:
        parent_categories: QuerySet[Category] = self.get_categories(
            only_active=only_active
        ).filter(parent__isnull=True)
        subcategories: QuerySet[Category] = self.get_categories(
            only_active=only_active
        )

        return parent_categories.prefetch_related(
            Prefetch(lookup="subcategories", queryset=subcategories)
        )

    def get_category(
        self, *, category_slug: str, only_active: bool = True
    ) -> Optional[Category]:
        return (
            self.get_categories(only_active=only_active)
            .filter(slug=category_slug)
            .first()
        )

    def get_hierarchy(self, *, category: Category) -> List[Category]:
        hierarchy: List[Category] = []
        ancestor: Optional[Category] = category

        while ancestor is not None:
            hierarchy.append(ancestor)
            ancestor = ancestor.parent

        hierarchy.reverse()

        return hierarchy
