from typing import Optional

from django.db import IntegrityError, transaction
from django.db.models import QuerySet

from apps.accounts.models import User
from apps.carts.choices import CartStatus
from apps.carts.exceptions import (
    CartItemAlreadyExistsError,
    CartItemNotFoundError,
    InsufficientStockError,
    InvalidCartItemQuantityError,
    ProductUnavailableError,
)
from apps.carts.models import Cart, CartItem
from apps.carts.selectors import CartSelector
from apps.catalog.models import Product
from apps.catalog.selectors import ProductSelector


class CartService:

    @transaction.atomic
    def get_or_create_active_cart_for_user(self, *, user: User) -> Cart:
        cart: Optional[Cart] = CartSelector().get_active_cart_for_user(
            user=user,
        )

        if cart is not None:
            return cart

        return Cart.objects.create(
            user=user,
            cart_status=CartStatus.ACTIVE,
        )

    @transaction.atomic
    def clear_cart(self, *, cart: Cart) -> None:
        cart_items: QuerySet[CartItem] = (
            CartSelector().get_cart_items_for_cart(cart=cart)
        )
        cart_items.delete()

    @transaction.atomic
    def delete_cart_item(self, *, cart: Cart, cart_item_pk: int) -> None:
        cart_item: Optional[CartItem] = CartSelector().get_cart_item_for_cart(
            cart=cart,
            cart_item_pk=cart_item_pk,
        )

        if cart_item is None:
            raise CartItemNotFoundError()

        cart_item.delete()

    @transaction.atomic
    def create_cart_item(
        self, *, cart: Cart, product_pk: int, quantity: int = 1
    ) -> CartItem:
        if quantity <= 0:
            raise InvalidCartItemQuantityError()

        product: Optional[Product] = ProductSelector().get_product_for_update(
            product_pk=product_pk,
        )

        if product is None:
            raise ProductUnavailableError()

        if product.stock < quantity:
            raise InsufficientStockError()

        try:
            return CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity,
            )
        except IntegrityError as error:
            raise CartItemAlreadyExistsError() from error

    @transaction.atomic
    def adjust_cart_item_quantity(
        self, *, cart: Cart, cart_item_pk: int, delta: int
    ) -> CartItem:
        cart_item: Optional[CartItem] = CartSelector().get_cart_item_for_cart(
            cart=cart,
            cart_item_pk=cart_item_pk,
        )

        if not cart_item:
            raise CartItemNotFoundError()

        new_quantity: int = cart_item.quantity + delta

        if new_quantity <= 0:
            raise InvalidCartItemQuantityError()

        product: Optional[Product] = ProductSelector().get_product_for_update(
            product_pk=cart_item.product.pk,
        )

        if product is None:
            raise ProductUnavailableError()

        if delta > 0 and product.stock < new_quantity:
            raise InsufficientStockError()

        cart_item.quantity = new_quantity
        cart_item.save(update_fields=["quantity"])

        return cart_item

    @transaction.atomic
    def has_unavailable_cart_items(self, *, cart: Cart) -> bool:
        cart_items: QuerySet[CartItem] = (
            CartSelector().get_cart_items_for_cart(cart=cart)
        )

        for cart_item in cart_items:
            product: Product = cart_item.product

            if not product.is_active or product.stock <= 0:
                return True

        return False

    @transaction.atomic
    def validate_cart_item_quantities(self, *, cart: Cart) -> bool:
        was_modified: bool = False

        cart_items: QuerySet[CartItem] = (
            CartSelector().get_cart_items_for_cart(cart=cart)
        )

        for cart_item in cart_items:
            product: Product = cart_item.product

            if not product.stock:
                continue

            if cart_item.quantity > product.stock:
                cart_item.quantity = product.stock
                cart_item.save(update_fields=["quantity"])
                was_modified = True

        return was_modified
