from typing import Any, Dict, List

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django_filters.views import FilterView

from apps.catalog.filters import ProductSearchFilter
from apps.catalog.models import Product
from apps.catalog.selectors import ProductSelector


class ProductSearchListView(FilterView):
    template_name = "catalog/product_search_list.html"
    context_object_name = "products"
    paginate_by = 20
    paginate_orphans = 4
    filterset_class = ProductSearchFilter

    def get_template_names(self) -> List[str]:
        if self.request.htmx:  # type: ignore
            return ["catalog/includes/_product_list.html"]
        return [self.template_name]

    def get(self, request: HttpRequest, **kwargs: Any) -> HttpResponse:
        if not request.GET.get(key="q", default="").strip():
            return redirect(to="pages:home")
        return super().get(request, **kwargs)

    def get_queryset(self) -> QuerySet[Product]:
        return ProductSelector().get_products()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"name": _("Home"), "url": reverse_lazy(viewname="pages:home")},
            {
                "name": _("Catalog"),
                "url": reverse_lazy(viewname="catalog:category-list"),
            },
            {
                "name": _("Search by query"),
                "url": reverse_lazy(viewname="catalog:product-search-list"),
            },
        ]
        return context
