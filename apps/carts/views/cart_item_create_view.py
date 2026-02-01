from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.carts.repositories import CartRepository


class CartItemCreateView(LoginRequiredMixin, View):
    """View for creating the cart item in user active cart."""

    def post(self, request: HttpRequest, product_slug: str) -> HttpResponse:
        """Create a cart item and redirect to HTTP Referer."""
        CartRepository.create_cart_item(
            user=request.user, product_slug=product_slug  # type: ignore
        )
        messages.success(
            request,
            _(
                "The product has been successfully added to your cart. "
                "The price has been updated."
            ),
        )
        return redirect(request.META.get("HTTP_REFERER", "/"))
