from django.db.models import QuerySet

from apps.orders.models import Order, OrderItem


class OrderSelector:

    def get_order_items(self, *, order: Order) -> QuerySet[OrderItem]:
        return order.order_items.all()

    def get_current_count_orders_per_year(self, *, year: int) -> int:
        return Order.objects.filter(created_at__year=year).count()
