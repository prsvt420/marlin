from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView

from apps.catalog.models import Category
from apps.catalog.selectors import CategorySelector


class CategoryListView(ListView):
    template_name = "catalog/redesign/category_list.html"
    context_object_name = "parent_categories"
    extra_context = {
        "breadcrumbs": [
            {"name": _("Home"), "url": reverse_lazy("pages:home")},
            {
                "name": _("Catalog"),
                "url": reverse_lazy("catalog:category-list"),
            },
        ]
    }

    def get_queryset(self) -> QuerySet[Category]:
        return CategorySelector().get_parent_categories()
