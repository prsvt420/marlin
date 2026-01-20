from django.db.models import QuerySet
from django.views import generic

from apps.catalog.models import Category
from apps.catalog.repositories import CategoryRepository


class CategoryListView(generic.ListView):
    """View for displaying the category list."""

    model = Category
    template_name = "catalog/category_list.html"
    context_object_name = "parent_categories"

    def get_queryset(self) -> QuerySet[Category]:
        """Return all active categories with parents."""
        return CategoryRepository.get_parents()
