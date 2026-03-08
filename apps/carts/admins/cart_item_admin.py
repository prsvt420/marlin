from django.contrib import admin

from apps.carts.models import CartItem
from apps.core.admins import BaseModelAdmin


@admin.register(CartItem)
class CartItemAdmin(BaseModelAdmin):
    list_display = (
        "cart",
        "product",
        "quantity",
        "price_snapshot",
        "total_price",
        "updated_at",
        "created_at",
    )
    readonly_fields = (
        "price_snapshot",
        "total_price",
        "created_at",
        "updated_at",
    )
