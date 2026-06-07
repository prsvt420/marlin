from django.contrib import admin
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import ChoicesDropdownFilter
from unfold.decorators import display

from apps.core.admins import BaseModelAdmin
from apps.orders.admins.order_item_inline_admin import OrderItemInline
from apps.orders.choices import OrderStatus, PaymentStatus
from apps.orders.models import Order


@admin.register(Order)
class OrderAdmin(BaseModelAdmin):
    inlines = (OrderItemInline,)
    list_display = (
        "number",
        "user",
        "display_order_status",
        "display_payment_status",
        "delivery_method",
        "payment_method",
        "total_price",
        "created_at",
    )
    fields = (
        "number",
        "user",
        "cart",
        "order_status",
        "payment_status",
        "delivery_method",
        "delivery_address",
        "payment_method",
        "recipient_name",
        "recipient_email",
        "recipient_phone_number",
        "comment",
        "total_price",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "number",
        "user",
        "cart",
        "delivery_method",
        "delivery_address",
        "payment_method",
        "recipient_name",
        "recipient_email",
        "recipient_phone_number",
        "comment",
        "total_price",
        "created_at",
        "updated_at",
    )
    list_filter = (
        ("order_status", ChoicesDropdownFilter),
        ("payment_status", ChoicesDropdownFilter),
        ("delivery_method", ChoicesDropdownFilter),
        ("payment_method", ChoicesDropdownFilter),
    )
    search_fields = (
        "number",
        "user__email",
        "recipient_name",
        "recipient_email",
        "recipient_phone_number",
    )
    search_help_text = _(
        "Search by order number, user, recipient email, name or phone"
    )
    list_select_related = ("user",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    @display(
        description=_("Order status"),
        label={
            OrderStatus.PENDING: "warning",
            OrderStatus.CONFIRMED: "info",
            OrderStatus.ASSEMBLING: "info",
            OrderStatus.SHIPPED: "info",
            OrderStatus.COMPLETED: "success",
            OrderStatus.CANCELLED: "danger",
        },
    )
    def display_order_status(self, obj: Order) -> str:
        return obj.order_status

    @display(
        description=_("Payment status"),
        label={
            PaymentStatus.PENDING: "warning",
            PaymentStatus.PAID: "success",
            PaymentStatus.FAILED: "danger",
            PaymentStatus.REFUNDED: "info",
        },
    )
    def display_payment_status(self, obj: Order) -> str:
        return obj.payment_status
