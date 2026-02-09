from typing import Any, Dict

from django.db.models import QuerySet
from django.views.generic import DetailView

from apps.carts.repositories import CartRepository
from apps.catalog.models import Product
from apps.catalog.selectors import CategorySelector, ProductSelector


class ProductDetailView(DetailView):

    template_name = "catalog/product_detail.html"
    context_object_name = "product"
    slug_url_kwarg = "product_slug"

    def get_queryset(self) -> QuerySet[Product]:
        category_slug: str = self.kwargs["category_slug"]
        return ProductSelector().get_products(category_slug=category_slug)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["hierarchy_categories"] = CategorySelector().get_hierarchy(
            category=self.object.category
        )

        if self.request.user.is_authenticated:
            context["cart_product_pks"] = CartRepository().get_product_ids(
                self.request.user
            )

        return context
