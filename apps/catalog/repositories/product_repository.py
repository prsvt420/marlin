from typing import Optional

from django.db.models import Prefetch, QuerySet

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
        *, search_query: Optional[str] = None, only_active: bool = True
    ) -> QuerySet[Product]:
        """Return a filtered queryset of products.

        Args:
            search_query (Optional[str]): The query to search.
            only_active (bool): If True, returns only active products.
            Default True.

        Returns:
            QuerySet[Product]: A queryset containing active Product
            objects filtered according to the provided criteria.
        """
        queryset: QuerySet[Product] = ProductRepository.all()

        if only_active:
            queryset = queryset.filter(is_active=True)

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset
