from typing import Set

from django.db.models import Prefetch, QuerySet

from apps.carts.models import Cart, CartItem
from apps.catalog.models import Product
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

    @staticmethod
    def delete_cart_item(cart: Cart, product_slug: str) -> None:
        """Delete a cart item from the cart."""
        cart.cart_items.filter(product__slug=product_slug).delete()

    @staticmethod
    def create_cart_item(cart: Cart, product_slug: str) -> None:
        """Create a cart item in the cart."""
        product: Product = ProductRepository.get_by_slug(slug=product_slug)
        cart.cart_items.get_or_create(cart=cart, product=product)

    @staticmethod
    def get_existing_products(cart: Cart) -> Set[int]:
        """Return a set of products that exists in the cart."""
        existing_products: Set[int] = set(
            cart.cart_items.values_list("product__pk", flat=True)
        )
        return existing_products
