from typing import Optional

from django.http import HttpRequest
from unfold.admin import TabularInline

from apps.orders.models import OrderItem


class OrderItemInline(TabularInline):
    model = OrderItem
    fields = (
        "product",
        "product_name_snapshot",
        "quantity",
        "price_snapshot",
        "total_price",
        "created_at",
    )
    readonly_fields = fields
    extra = 0
    can_delete = False
    show_change_link = True
    tab = True

    def has_add_permission(
        self, request: HttpRequest, obj: Optional[OrderItem] = None
    ) -> bool:
        return False
