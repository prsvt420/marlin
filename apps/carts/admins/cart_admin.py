from decimal import Decimal

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.carts.admins import CartItemInline
from apps.carts.models import Cart
from apps.carts.selectors import CartSelector


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = (
        "user",
        "cart_status",
        "total_quantity",
        "total_price",
    )
    list_editable = ("cart_status",)
    list_filter = ("cart_status",)
    search_fields = (
        "user__email",
        "user__username",
    )
    search_help_text = _("Search by email and username")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    fields = (
        "user",
        "cart_status",
        ("created_at", "updated_at"),
    )
    inlines = (CartItemInline,)

    @admin.display(description=_("Total price"))
    def total_price(self, obj: Cart) -> Decimal:
        return CartSelector().get_cart_prices(cart=obj)["total_price"]

    @admin.display(description=_("Total quantity"))
    def total_quantity(self, obj: Cart) -> int:
        return obj.total_quantity
