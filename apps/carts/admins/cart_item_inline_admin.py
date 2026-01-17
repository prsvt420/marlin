from django.contrib import admin

from apps.carts.models import CartItem


class CartItemInline(admin.TabularInline):
    """Configuration for inline administration of the CartItem model."""

    model = CartItem
    extra = 0
    readonly_fields = ("price_snapshot",)
