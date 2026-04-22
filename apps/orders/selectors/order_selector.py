from django.db.models import QuerySet

from apps.orders.models import Order, OrderItem


class OrderSelector:

    def get_order_items(self, *, order: Order) -> QuerySet[OrderItem]:
        return order.order_items.all()
