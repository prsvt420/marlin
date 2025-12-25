from decimal import Decimal

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.carts.models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """Inline for cart item."""

    model = CartItem
    extra = 0
    readonly_fields = ("price_snapshot",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin configuration for Cart model."""

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

    @admin.display(description=_("Total quantity"))
    def total_quantity(self, obj: Cart) -> int:
        """Return the total quantity of items in the cart.

        Returns:
            int: Total number of items in the cart.
        """
        return obj.get_total_quantity()

    @admin.display(description=_("Total price"))
    def total_price(self, obj: Cart) -> Decimal:
        """Return the total price of all items in the cart.

        Returns:
            Decimal: Final cart price.
        """
        return obj.get_total_price()
