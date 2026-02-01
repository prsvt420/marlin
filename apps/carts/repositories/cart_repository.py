from typing import Set

from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import Prefetch, QuerySet

from apps.carts.choices import CartStatus
from apps.carts.models import Cart
from apps.carts.repositories import CartItemRepository


class CartRepository:
    """Repository for accessing Cart model."""

    @staticmethod
    def all() -> QuerySet[Cart]:
        """Return all carts with related prefetched."""
        return Cart.objects.all().prefetch_related(
            Prefetch(
                "cart_items",
                queryset=CartItemRepository.all(),
            ),
        )

    @staticmethod
    def get_user_active_cart(user: AbstractBaseUser) -> Cart:
        """Retrieve a active cart by user or create if not found."""
        cart, created = Cart.objects.get_or_create(
            user=user, cart_status=CartStatus.ACTIVE
        )

        if not created:
            cart = (
                CartRepository.all().filter(pk=cart.pk).first()  # type: ignore
            )

        return cart

    @staticmethod
    def clear_cart(user: AbstractBaseUser) -> None:
        """Clear all cart items from the user active cart."""
        cart: Cart = CartRepository.get_user_active_cart(user)
        CartItemRepository.clear_cart(cart)

    @staticmethod
    def delete_cart_item(user: AbstractBaseUser, product_slug: str) -> None:
        """Delete a cart item from the user active cart."""
        cart: Cart = CartRepository.get_user_active_cart(user)
        CartItemRepository.delete_cart_item(
            cart=cart, product_slug=product_slug
        )

    @staticmethod
    def create_cart_item(user: AbstractBaseUser, product_slug: str) -> None:
        """Create a cart item in the user active cart."""
        cart: Cart = CartRepository.get_user_active_cart(user)
        CartItemRepository.create_cart_item(
            cart=cart, product_slug=product_slug
        )

    @staticmethod
    def get_existing_products(user: AbstractBaseUser) -> Set[int]:
        """Return a set of products that exists in the user active cart."""
        cart: Cart = CartRepository.get_user_active_cart(user)
        return CartItemRepository.get_existing_products(cart=cart)
