from django.db.models import Prefetch, QuerySet

from apps.catalog.models import Product, ProductAttribute


class ProductRepository:
    """Repository for Product model database operations."""

    @staticmethod
    def find_active() -> QuerySet[Product]:
        """Return a queryset of products marked as active.

        Only products with `is_active=True` are included in the queryset.

        Returns:
            QuerySet[Product]: A Django QuerySet containing active Product
            objects.
        """
        return (
            Product.objects.filter(is_active=True)
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
    def find_by_search_query(search_query: str) -> QuerySet[Product]:
        """Return a queryset of products whose names contain the search query.

        Only products with `is_active=True` are included in the queryset.

        Args:
            search_query (str): The query to search for in product names.

        Returns:
            QuerySet[Product]: A Django QuerySet of matching Product objects.
        """
        return ProductRepository.find_active().filter(
            name__icontains=search_query
        )
