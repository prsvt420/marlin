from typing import Any, Dict, List, Optional

from django.db.models import QuerySet
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django_filters.views import FilterView

from apps.catalog.filters import ProductFilter
from apps.catalog.models import Category, Product
from apps.catalog.selectors import CategorySelector, ProductSelector


class ProductListView(FilterView):
    template_name = "catalog/redesign/product_list.html"
    context_object_name = "products"
    paginate_by = 20
    paginate_orphans = 4
    filterset_class = ProductFilter

    def get_template_names(self) -> List[str]:
        if self.request.htmx:  # type: ignore
            return ["catalog/redesign/includes/_product_list_htmx.html"]
        return [self.template_name]

    @property
    def category_slug(self) -> str:
        return self.kwargs["category_slug"]

    @property
    def category(self) -> Category:
        category: Optional[Category] = CategorySelector().get_category(
            category_slug=self.category_slug
        )

        if category is None:
            raise Http404

        return category

    def get_queryset(self) -> QuerySet[Product]:
        category_slug: Optional[str] = self.category_slug

        return ProductSelector().get_products(
            category_slug=category_slug,
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["breadcrumbs"] = [
            {"name": _("Home"), "url": reverse_lazy(viewname="pages:home")},
            {
                "name": _("Catalog"),
                "url": reverse_lazy(viewname="catalog:category-list"),
            },
            {
                "name": context["category"],
                "url": context["category"].get_absolute_url(),
            },
        ]
        return context
