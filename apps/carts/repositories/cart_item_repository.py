from typing import Optional, Set

from django.db import transaction
from django.db.models import Prefetch, QuerySet

from apps.carts.models import Cart, CartItem
from apps.catalog.models import Product
from apps.catalog.selectors import ProductSelector


class CartItemRepository:
    """Repository for accessing CartItem model."""

    def get_all(self) -> QuerySet[CartItem]:
        """Return all cart items with related prefetched."""
        return CartItem.objects.prefetch_related(
            Prefetch(
                "product",
                ProductSelector().get_products(),
            )
        )

    def get_available(self, cart: Cart) -> QuerySet[CartItem]:
        """Return available cart items from the given cart."""
        return cart.cart_items.filter(
            product__is_active=True, product__stock__gt=0
        )

    def get_unavailable(self, cart: Cart) -> QuerySet[CartItem]:
        """Return unavailable cart items from the given cart."""
        return cart.cart_items.exclude(
            product__is_active=True, product__stock__gt=0
        )

    def delete_all(self, cart: Cart) -> None:
        """Delete all cart items from the given cart."""
        cart.cart_items.all().delete()

    def delete(self, cart: Cart, product_slug: str) -> None:
        """Delete a cart item by product slug from the given cart."""
        cart.cart_items.filter(product__slug=product_slug).delete()

    def create(self, cart: Cart, product_slug: str) -> None:
        """Create a cart item in the given cart."""
        product: Optional[Product] = ProductSelector().get_product(
            product_slug=product_slug
        )
        cart.cart_items.get_or_create(cart=cart, product=product)

    @transaction.atomic
    def decrement_quantity(self, cart: Cart, product_slug: str) -> None:
        """Decrease the quantity of a cart item in the given cart."""
        cart_item: Optional[CartItem] = (
            cart.cart_items.select_for_update()
            .filter(product__slug=product_slug)
            .first()
        )

        if not cart_item:
            return

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save(update_fields=["quantity"])

    @transaction.atomic
    def increment_quantity(self, cart: Cart, product_slug: str) -> None:
        """Increase the quantity of a cart item in the given cart."""
        cart_item: Optional[CartItem] = (
            cart.cart_items.select_for_update()
            .filter(product__slug=product_slug)
            .first()
        )

        if not cart_item:
            return

        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save(update_fields=["quantity"])

    def get_product_ids(self, cart: Cart) -> Set[int]:
        """Return the set of all product IDs in the given cart."""
        product_ids: Set[int] = set(
            cart.cart_items.values_list("product__pk", flat=True)
        )
        return product_ids
