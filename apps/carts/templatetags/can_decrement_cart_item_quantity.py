from decimal import Decimal

from django import template

from apps.carts.models import CartItem

register: template.Library = template.Library()


@register.simple_tag
def can_decrement_cart_item_quantity(cart_item: CartItem) -> bool:
    step: Decimal = cart_item.product.weight_step or Decimal("1")
    return cart_item.quantity > step
