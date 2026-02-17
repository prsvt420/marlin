from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.carts.models import CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ("price_snapshot", "total_price")

    @admin.display(description=_("Total price"))
    def total_price(self, obj: CartItem) -> str:
        return obj.total_price
