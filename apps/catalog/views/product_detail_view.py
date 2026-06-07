from typing import Any, Dict, List

from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView

from apps.catalog.models import Product
from apps.catalog.selectors import CategorySelector, ProductSelector
from apps.reviews.selectors import ProductReviewSelector


class ProductDetailView(DetailView):
    template_name = "catalog/product_detail.html"
    context_object_name = "product"
    slug_url_kwarg = "product_slug"

    def get_queryset(self) -> QuerySet[Product]:
        category_slug: str = self.kwargs["category_slug"]
        return ProductSelector().get_products(category_slug=category_slug)

    @property
    def breadcrumbs(self) -> List[Dict[str, Any]]:
        breadcrumbs: List[Dict[str, Any]] = [
            {"name": _("Home"), "url": reverse(viewname="pages:home")},
            {
                "name": _("Catalog"),
                "url": reverse(viewname="catalog:category-list"),
            },
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
        context["similar_products"] = ProductSelector().get_similar_products(
            product=self.object
        )

        if self.request.user.is_authenticated:
            product_review_selector = ProductReviewSelector()
            can_review_product: bool = (
                product_review_selector.can_user_review_product(
                    user=self.request.user,  # type: ignore
                    product_pk=self.object.pk,
                )
            )
            context["can_review_product"] = can_review_product

            if can_review_product:
                context["product_review"] = (
                    product_review_selector.get_user_product_review(
                        user=self.request.user,  # type: ignore
                        product_pk=self.object.pk,
                    )
                )

        return context
