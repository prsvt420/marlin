from typing import Set

from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import Prefetch, QuerySet

from apps.carts.choices import CartStatus
from apps.carts.models import Cart
from apps.carts.repositories import CartItemRepository


class CartRepository:
    """Repository for accessing Cart model."""

    def get_all(self) -> QuerySet[Cart]:
        """Return all carts with related prefetched."""
        return Cart.objects.all().prefetch_related(
            Prefetch(
                "cart_items",
                queryset=CartItemRepository().get_all(),
            ),
        )

    def get_user_active(self, user: AbstractBaseUser) -> Cart:
        """Retrieve a active cart by user or create if not found."""
        cart, created = Cart.objects.get_or_create(
            user=user, cart_status=CartStatus.ACTIVE
        )

        if not created:
            cart = self.get_all().filter(pk=cart.pk).first()  # type: ignore

        return cart

    def clear(self, user: AbstractBaseUser) -> None:
        """Clear all cart items from the user active cart."""
        cart: Cart = self.get_user_active(user=user)
        CartItemRepository().delete_all(cart=cart)

    def delete_item(self, user: AbstractBaseUser, product_slug: str) -> None:
        """Delete a cart item by product slug from the user active cart."""
        cart: Cart = self.get_user_active(user=user)
        CartItemRepository().delete(cart=cart, product_slug=product_slug)

    def create_item(self, user: AbstractBaseUser, product_slug: str) -> None:
        """Create a cart item in the user active cart."""
        cart: Cart = self.get_user_active(user=user)
        CartItemRepository().create(cart=cart, product_slug=product_slug)

    def decrement_item_quantity(
        self, user: AbstractBaseUser, product_slug: str
    ) -> None:
        """Decrease the quantity of a cart item in the user active cart."""
        cart: Cart = self.get_user_active(user=user)
        CartItemRepository().decrement_quantity(
            cart=cart, product_slug=product_slug
        )

    def increment_item_quantity(
        self, user: AbstractBaseUser, product_slug: str
    ) -> None:
        """Increase the quantity of a cart item in the user active cart."""
        cart: Cart = self.get_user_active(user=user)
        CartItemRepository().increment_quantity(
            cart=cart, product_slug=product_slug
        )

    def get_product_ids(self, user: AbstractBaseUser) -> Set[int]:
        """Return the set of all product IDs in the user active cart."""
        cart: Cart = self.get_user_active(user=user)
        return CartItemRepository().get_product_ids(cart=cart)
