from typing import Optional

from django.contrib import admin
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from apps.core.admins import BaseModelAdmin
from apps.orders.models import OrderItem


@admin.register(OrderItem)
class OrderItemAdmin(BaseModelAdmin):
    list_display = (
        "order",
        "product_name_snapshot",
        "quantity",
        "price_snapshot",
        "total_price",
        "created_at",
    )
    fields = (
        "order",
        "product",
        "product_name_snapshot",
        "quantity",
        "price_snapshot",
        "total_price",
        "created_at",
        "updated_at",
    )
    readonly_fields = fields
    search_fields = (
        "order__number",
        "product_name_snapshot",
        "product__name",
    )
    search_help_text = _("Search by order number or product name")
    list_select_related = ("order", "product")
    date_hierarchy = "created_at"

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: Optional[OrderItem] = None
    ) -> bool:
        return False
