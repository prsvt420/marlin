from django.db.models import Prefetch, QuerySet

from apps.carts.models import Cart, CartItem
from apps.catalog.repositories import ProductRepository


class CartItemRepository:
    """Repository for accessing CartItem model."""

    @staticmethod
    def all() -> QuerySet[CartItem]:
        """Return all cart items with related prefetched."""
        return CartItem.objects.prefetch_related(
            Prefetch(
                "product",
                ProductRepository.all(),
            )
        )

    @staticmethod
    def clear_cart(cart: Cart) -> None:
        """Clear all cart items from the cart."""
        cart.cart_items.all().delete()
