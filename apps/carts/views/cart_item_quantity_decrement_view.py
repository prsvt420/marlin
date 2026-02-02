from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.carts.repositories import CartRepository


class CartItemQuantityDecrementView(LoginRequiredMixin, View):
    """View for decrementing the cart item quantity in user active cart."""

    def post(self, request: HttpRequest, product_slug: str) -> HttpResponse:
        """Decrease cart item quantity and redirect to cart detail."""
        CartRepository.decrement_item_quantity(
            user=request.user, product_slug=product_slug  # type: ignore
        )
        messages.success(
            request,
            _(
                "The product quantity has been successfully "
                "decreased in your cart. The price has been updated."
            ),
        )
        return redirect("carts:cart_detail")
