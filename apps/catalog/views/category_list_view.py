from django.db.models import QuerySet
from django.views.generic import ListView

from apps.catalog.models import Category
from apps.catalog.selectors import CategorySelector


class CategoryListView(ListView):
    template_name = "catalog/category_list.html"
    context_object_name = "parent_categories"

    def get_queryset(self) -> QuerySet[Category]:
        return CategorySelector().get_parent_categories()
