from typing import Optional

from django.db.models import (
    DecimalField,
    ExpressionWrapper,
    F,
    Prefetch,
    Q,
    QuerySet,
)

from apps.catalog.models import Product, ProductAttribute


class ProductRepository:
    """Repository for accessing Product model."""

    @staticmethod
    def all() -> QuerySet[Product]:
        """Return all products with related prefetched."""
        return (
            Product.objects.all()
            .select_related("category", "product_nutrition")
            .prefetch_related(
                "product_images",
                Prefetch(
                    "product_attributes",
                    queryset=ProductAttribute.objects.select_related(
                        "attribute"
                    ),
                ),
            )
        )

    @staticmethod
    def filter(
        *,
        search_query: Optional[str] = None,
        only_active: bool = True,
        order_field: Optional[str] = None,
        category_slug: Optional[str] = None,
    ) -> QuerySet[Product]:
        """Return filtered products."""
        queryset: QuerySet[Product] = ProductRepository.all()

        if only_active:
            queryset = queryset.filter(is_active=True)

        if category_slug:
            queryset = queryset.filter(
                Q(category__slug=category_slug)
                | Q(category__parent__slug=category_slug),  # noqa: W503
            )

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        if order_field in ("final_price", "-final_price"):
            queryset = queryset.annotate(
                final_price=ExpressionWrapper(
                    expression=F("price") * (1 - F("discount") / 100.0),
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                )
            )

        if order_field:
            queryset = queryset.order_by(order_field)

        return queryset
