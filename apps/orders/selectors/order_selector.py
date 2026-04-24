from typing import Optional

from django.db.models import QuerySet

from apps.orders.models import Order, OrderItem


class OrderSelector:

    def get_order_items(self, *, order: Order) -> QuerySet[OrderItem]:
        return order.order_items.all()

    def get_order_by_number(self, *, order_number: str) -> Optional[Order]:
        return Order.objects.filter(number=order_number).first()
