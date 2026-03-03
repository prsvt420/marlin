from typing import Any, Dict, Optional

from django.db.models import QuerySet
from django.http import Http404
from django_filters.views import FilterView

from apps.carts.selectors import CartSelector
from apps.catalog.filters import ProductFilter
from apps.catalog.models import Category, Product
from apps.catalog.selectors import CategorySelector, ProductSelector


class ProductListView(FilterView):
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 12
    paginate_orphans = 4
    filterset_class = ProductFilter

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

        if self.request.user.is_authenticated:
            context[
                "cart_product_pks"
            ] = CartSelector().get_user_active_cart_product_pks(
                user=self.request.user  # type: ignore
            )

        return context
