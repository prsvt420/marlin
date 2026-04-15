from typing import Any, Dict

from django.http import HttpRequest

from apps.carts.models import Cart, CartItem
from apps.carts.selectors import CartSelector
from apps.carts.services import CartService


def cart(request: HttpRequest) -> Dict[str, Any]:
    context: Dict[str, Any] = {
        "cart": None,
        "cart_items_map": {},
    }

    if not request.user.is_authenticated:
        return context

    cart: Cart = CartService().get_or_create_active_cart_for_user(
        user=request.user  # type: ignore
    )
    cart_items_map: Dict[int, CartItem] = CartSelector().get_cart_items_map(
        cart=cart
    )
    cart_prices = CartSelector().get_cart_prices(cart=cart)

    context["cart"] = cart
    context["cart_items_map"] = cart_items_map
    context["cart_prices"] = cart_prices
    context["available_cart_items"] = CartSelector().get_available_cart_items(
        cart=cart
    )
    context["unavailable_cart_items"] = (
        CartSelector().get_unavailable_cart_items(cart=cart)
    )

    return context
