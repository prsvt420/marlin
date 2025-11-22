from typing import Optional

from django.db.models import (
    DecimalField,
    ExpressionWrapper,
    F,
    Prefetch,
    QuerySet,
)

from apps.catalog.models import Product, ProductAttribute


class ProductRepository:
    """Repository for Product model database operations."""

    @staticmethod
    def all() -> QuerySet[Product]:
        """Return a queryset of all products with related data preloaded.

        Returns:
            QuerySet[Product]: A queryset containing all Product objects
            with related data preloaded.
        """
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
    ) -> QuerySet[Product]:
        """Return a filtered queryset of products.

        Args:
            search_query (Optional[str]): The query to search.
            only_active (bool): If True, returns only active products.
            Default True.
            order_field (Optional[str]): Field to order by.

        Returns:
            QuerySet[Product]: A queryset containing active Product
            objects filtered according to the provided criteria.
        """
        queryset: QuerySet[Product] = ProductRepository.all()

        if only_active:
            queryset = queryset.filter(is_active=True)

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
