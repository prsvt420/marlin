from typing import Optional

from django.db.models import (
    DecimalField,
    ExpressionWrapper,
    F,
    Prefetch,
    Q,
    QuerySet,
)
from django.shortcuts import get_object_or_404

from apps.catalog.models import Product, ProductAttribute


class ProductRepository:
    """Repository for accessing Product model."""

    def get_all(self) -> QuerySet[Product]:
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

    def get_filtered(
        self,
        *,
        search_query: Optional[str] = None,
        only_active: bool = True,
        order_field: Optional[str] = None,
        category_slug: Optional[str] = None,
    ) -> QuerySet[Product]:
        """Return filtered products."""
        queryset: QuerySet[Product] = self.get_all()

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

    def get_by_slug(self, slug: str) -> Product:
        """Retrieve a product by slug or raise 404 if not found."""
        return get_object_or_404(Product, slug=slug)
