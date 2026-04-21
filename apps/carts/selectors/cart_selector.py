from decimal import ROUND_HALF_UP, Decimal
from typing import Dict, List, Optional

from django.db.models import Prefetch, QuerySet, Sum

from apps.accounts.models import User
from apps.carts.choices import CartStatus
from apps.carts.models import Cart, CartItem
from apps.catalog.selectors import ProductSelector


class CartSelector:

    def get_carts(self) -> QuerySet[Cart]:
        return Cart.objects.prefetch_related(
            Prefetch(
                lookup="cart_items",
                queryset=CartItem.objects.prefetch_related(
                    Prefetch(
                        lookup="product",
                        queryset=ProductSelector().get_products(
                            only_active=False
                        ),
                    )
                ),
            )
        )

    def get_cart_items(self, *, cart: Cart) -> QuerySet[CartItem]:
        return cart.cart_items.all()

    def get_cart_item(
        self, *, cart: Cart, cart_item_pk: int
    ) -> Optional[CartItem]:
        return cart.cart_items.filter(pk=cart_item_pk).first()

    def get_active_cart_for_user(self, *, user: User) -> Optional[Cart]:
        return (
            self.get_carts()
            .filter(user=user, cart_status=CartStatus.ACTIVE)
            .first()
        )

    def get_cart_items_map(self, *, cart: Cart) -> Dict[int, CartItem]:
        return {
            cart_item.product_id: cart_item
            for cart_item in cart.cart_items.all()
        }

    def get_cart_products_total_price(self, *, cart: Cart) -> Decimal:
        cart_items: QuerySet[CartItem] = self.get_cart_items(cart=cart).filter(
            product__is_available=True
        )

        total_price: Decimal = cart_items.aggregate(
            total_price=Sum(
                "total_price",
            )
        )["total_price"] or Decimal("0.00")

        return total_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def get_cart_prices(self, *, cart: Cart) -> Dict[str, Decimal]:
        cart_products_total_price: Decimal = (
            self.get_cart_products_total_price(cart=cart)
        )
        cart_total_price: Decimal = cart_products_total_price

        cart_prices: Dict[str, Decimal] = {
            "products_total_price": cart_products_total_price,
            "total_price": cart_total_price,
        }

        return cart_prices

    def has_unavailable_cart_items(self, *, cart: Cart) -> bool:
        return cart.cart_items.filter(product__is_available=False).exists()

    def get_available_cart_items(self, *, cart: Cart) -> List[CartItem]:
        return [
            cart_item
            for cart_item in cart.cart_items.all()
            if cart_item.product.is_available
        ]

    def get_unavailable_cart_items(self, *, cart: Cart) -> List[CartItem]:
        return [
            cart_item
            for cart_item in cart.cart_items.all()
            if not cart_item.product.is_available
        ]

    def is_cart_empty(self, *, cart: Cart) -> bool:
        return not cart.cart_items.exists()
