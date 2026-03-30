from typing import Any, Dict, List

from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView

from apps.carts.selectors import CartSelector
from apps.catalog.models import Product
from apps.catalog.selectors import CategorySelector, ProductSelector


class ProductDetailView(DetailView):
    template_name = "catalog/redesign/product_detail.html"
    context_object_name = "product"
    slug_url_kwarg = "product_slug"

    def get_queryset(self) -> QuerySet[Product]:
        category_slug: str = self.kwargs["category_slug"]
        return ProductSelector().get_products(category_slug=category_slug)

    @property
    def breadcrumbs(self) -> List[Dict[str, Any]]:
        breadcrumbs: List[Dict[str, Any]] = [
            {"name": _("Catalog"), "url": reverse("catalog:category-list")},
        ]

        for ancestor in CategorySelector().get_hierarchy(
            category=self.object.category
        ):
            breadcrumbs.append(
                {"name": ancestor.name, "url": ancestor.get_absolute_url()}
            )

        breadcrumbs.append({"name": self.object.name})

        return breadcrumbs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["breadcrumbs"] = self.breadcrumbs

        if self.request.user.is_authenticated:
            context[
                "cart_product_pks"
            ] = CartSelector().get_user_active_cart_product_pks(
                user=self.request.user  # type: ignore
            )

        return context
