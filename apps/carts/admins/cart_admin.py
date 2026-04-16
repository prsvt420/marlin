from decimal import Decimal

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import ChoicesDropdownFilter
from unfold.decorators import display

from apps.carts.admins import CartItemInline
from apps.carts.choices import CartStatus
from apps.carts.models import Cart
from apps.carts.selectors import CartSelector
from apps.core.admins import BaseModelAdmin


@admin.register(Cart)
class CartAdmin(BaseModelAdmin):
    inlines = (CartItemInline,)
    list_display = (
        "user",
        "display_cart_status",
        "total_quantity",
        "total_price",
        "updated_at",
        "created_at",
    )
    fields = (
        "user",
        "cart_status",
        "total_price",
        "total_quantity",
        "created_at",
        "updated_at",
    )
    readonly_fields = (
        "total_price",
        "total_quantity",
        "created_at",
        "updated_at",
    )
    list_filter = (("cart_status", ChoicesDropdownFilter),)
    search_fields = ("user__email",)
    search_help_text = _("Search by email")
    autocomplete_fields = ("user",)

    @display(
        description=_("Status"),
        label={
            CartStatus.ACTIVE: "success",
            CartStatus.CONVERTED: "info",
            CartStatus.ABANDONED: "danger",
        },
    )
    def display_cart_status(self, obj: Cart) -> str:
        return obj.cart_status

    @display(description=_("Total price"))
    def total_price(self, obj: Cart) -> Decimal:
        return CartSelector().get_cart_prices(cart=obj)["total_price"]

    @display(description=_("Total quantity"))
    def total_quantity(self, obj: Cart) -> int:
        return obj.total_quantity
