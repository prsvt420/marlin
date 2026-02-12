from typing import Optional

from django.db.models import (
    Prefetch,
    Q,
    QuerySet,
)

from apps.catalog.models import Product
from apps.catalog.selectors import (
    ProductAttributeSelector,
    ProductImageSelector,
)


class ProductSelector:

    def get_products(
        self,
        *,
        search_query: Optional[str] = None,
        order_field: Optional[str] = None,
        category_slug: Optional[str] = None,
        only_active: bool = True,
    ) -> QuerySet[Product]:
        products: QuerySet[Product] = Product.objects.select_related(
            "category", "product_nutrition"
        ).prefetch_related(
            Prefetch(
                "product_images",
                queryset=ProductImageSelector().get_product_images(),
            ),
            Prefetch(
                "product_attributes",
                queryset=ProductAttributeSelector().get_product_attributes(),
            ),
        )

        if only_active:
            products = products.filter(is_active=True)

        if category_slug:
            products = products.filter(
                Q(category__slug=category_slug)
                | Q(category__parent__slug=category_slug),  # noqa: W503
            )

        if search_query:
            products = products.filter(name__icontains=search_query)

        if order_field:
            products = products.order_by(order_field)

        return products

    def get_product(
        self, *, product_slug: str, only_active: bool = True
    ) -> Optional[Product]:
        return (
            self.get_products(only_active=only_active)
            .filter(slug=product_slug)
            .first()
        )
