from typing import Any, Dict, Optional

from django.db.models import QuerySet
from django.http import Http404
from django.views.generic import ListView

from apps.carts.selectors import CartSelector
from apps.catalog.constants import ORDERING_OPTIONS
from apps.catalog.dataclasses import OrderingOption
from apps.catalog.models import Category, Product
from apps.catalog.selectors import CategorySelector, ProductSelector


class ProductListView(ListView):
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 12
    paginate_orphans = 4
    extra_context = {"ordering_options": ORDERING_OPTIONS}

    @property
    def ordering_option(self) -> OrderingOption:
        ordering_option_key: str = self.request.GET.get(
            key="sort", default="default"
        ).strip()

        return ORDERING_OPTIONS.get(
            ordering_option_key, ORDERING_OPTIONS["default"]
        )

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

    @property
    def search_query(self) -> Optional[str]:
        search_query: Optional[str] = self.request.GET.get(key="q")
        return search_query.strip() if search_query else None

    def get_queryset(self) -> QuerySet[Product]:
        search_query: Optional[str] = self.search_query
        order_field: Optional[str] = self.ordering_option.field
        category_slug: Optional[str] = self.category_slug

        return ProductSelector().get_products(
            search_query=search_query,
            order_field=order_field,
            category_slug=category_slug,
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["search_query"] = self.search_query
        context["current_ordering_option"] = self.ordering_option
        context["category"] = self.category

        if self.request.user.is_authenticated:
            context[
                "cart_product_pks"
            ] = CartSelector().get_user_active_cart_product_pks(
                user=self.request.user  # type: ignore
            )

        return context
