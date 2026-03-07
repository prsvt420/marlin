from typing import Optional

from django.db.models import (
    Prefetch,
    Q,
    QuerySet,
)

from apps.catalog.models import Product
from apps.catalog.selectors import (
    ProductImageSelector,
)


class ProductSelector:

    def get_products(
        self,
        *,
        category_slug: Optional[str] = None,
        only_active: bool = True,
    ) -> QuerySet[Product]:
        products: QuerySet[Product] = Product.objects.select_related(
            "category", "nutrition"
        ).prefetch_related(
            Prefetch(
                lookup="images",
                queryset=ProductImageSelector().get_product_images(),
            ),
        )

        if only_active:
            products = products.filter(is_active=True)

        if category_slug:
            products = products.filter(
                Q(category__slug=category_slug)
                | Q(category__parent__slug=category_slug),  # noqa: W503
            )

        return products

    def get_product(
        self, *, product_pk: int, only_active: bool = True
    ) -> Optional[Product]:
        return (
            self.get_products(only_active=only_active)
            .filter(pk=product_pk)
            .first()
        )

    def get_product_for_update(
        self, *, product_pk: int, only_active: bool = True
    ) -> Optional[Product]:
        return (
            self.get_products(only_active=only_active)
            .filter(pk=product_pk)
            .select_for_update(of=("self",))
            .first()
        )
