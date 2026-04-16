from django.utils.translation import gettext_lazy as _
from unfold.admin import TabularInline
from unfold.decorators import display

from apps.carts.models import CartItem


class CartItemInline(TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = (
        "price_snapshot",
        "total_price",
        "created_at",
        "updated_at",
    )
    tab = True
    autocomplete_fields = ("product",)

    @display(description=_("Total price"))
    def total_price(self, obj: CartItem) -> str:
        return obj.total_price
