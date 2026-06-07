from typing import Optional

from django.db.models import (
    Avg,
    Count,
    FloatField,
    Prefetch,
    Q,
    QuerySet,
    Value,
)
from django.db.models.functions import Coalesce

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
        products: QuerySet[Product] = (
            Product.objects.select_related("category", "nutrition")
            .prefetch_related(
                Prefetch(
                    lookup="images",
                    queryset=ProductImageSelector().get_product_images(),
                ),
            )
            .annotate(
                rating_average=Coalesce(
                    Avg("reviews__rating"),
                    Value(0.0),
                    output_field=FloatField(),
                ),
                rating_count=Count("reviews"),
            )
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
        products: QuerySet[Product] = Product.objects.select_for_update(
            of=("self",)
        )

        if only_active:
            products = products.filter(is_active=True)

        return products.filter(pk=product_pk).first()

    def get_similar_products(
        self, *, product: Product, limit: int = 12
    ) -> QuerySet[Product]:
        return (
            self.get_products(category_slug=product.category.slug)
            .exclude(pk=product.pk)
            .order_by("?")[:limit]
        )

    def get_popular_products(self, *, limit: int = 12) -> QuerySet[Product]:
        return self.get_products().order_by("?")[:limit]

    def get_new_products(self, *, limit: int = 12) -> QuerySet[Product]:
        return self.get_products().order_by("-created_at")[:limit]
