from decimal import Decimal
from typing import Any, Dict, List

from django.db import transaction
from django.db.models import Sum

from apps.accounts.models import User
from apps.carts.choices import CartStatus
from apps.carts.models import Cart, CartItem
from apps.carts.selectors import CartSelector
from apps.carts.services import CartService
from apps.catalog.services import ProductService
from apps.orders.exceptions import EmptyCartError
from apps.orders.models import Order, OrderItem
from apps.orders.selectors import OrderSelector


class OrderService:

    @transaction.atomic
    def recompute_total_price(self, *, order: Order) -> None:
        total_price: Decimal = OrderSelector().get_order_items(
            order=order
        ).aggregate(total=Sum("total_price"))["total"] or Decimal("0.00")
        order.total_price = total_price
        order.save(update_fields=["total_price"])

    @transaction.atomic
    def checkout(
        self, *, user: User, cart: Cart, **checkout_data: Dict[str, Any]
    ) -> Order:
        if CartSelector().is_cart_empty(cart=cart):
            raise EmptyCartError

        available_cart_items: List[CartItem] = (
            CartSelector().get_available_cart_items(cart=cart)
        )

        order: Order = Order.objects.create(
            user=user,
            cart=cart,
            **checkout_data,
        )
        order.number = f"ORD-{order.created_at.year}-{order.pk:06d}"
        order.save(update_fields=["number"])

        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price_snapshot=cart_item.price_snapshot,
                    product_name_snapshot=cart_item.product.name,
                )
                for cart_item in available_cart_items
            ]
        )

        for cart_item in available_cart_items:
            ProductService().decrease_stock(
                product_pk=cart_item.product.pk, quantity=cart_item.quantity
            )

        self.recompute_total_price(order=order)

        CartService().change_cart_status(
            cart=cart, new_status=CartStatus.CONVERTED
        )

        return order
