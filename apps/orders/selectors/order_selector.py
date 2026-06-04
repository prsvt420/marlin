from typing import Optional

from django.db.models import QuerySet

from apps.accounts.models import User
from apps.orders.models import Order, OrderItem


class OrderSelector:

    def get_order_items(self, *, order: Order) -> QuerySet[OrderItem]:
        return order.order_items.all()

    def get_order_by_number(self, *, order_number: str) -> Optional[Order]:
        return Order.objects.filter(number=order_number).first()

    def get_user_orders(self, *, user: User) -> QuerySet[Order]:
        return Order.objects.filter(user=user).prefetch_related(
            "order_items",
            "order_items__product",
            "order_items__product__images",
        )

    def get_user_recent_orders(
        self, *, user: User, limit: int = 5
    ) -> QuerySet[Order]:
        return self.get_user_orders(user=user)[:limit]
