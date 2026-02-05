from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.carts.repositories import CartRepository


class CartItemDeleteView(LoginRequiredMixin, View):
    """View for deleting the cart item from user active cart."""

    def post(self, request: HttpRequest, product_slug: str) -> HttpResponse:
        """Delete a cart item and redirect to cart detail."""
        CartRepository().delete_item(
            user=request.user, product_slug=product_slug  # type: ignore
        )
        messages.success(
            request,
            _(
                "The product has been successfully removed from the cart. "
                "The price has been updated."
            ),
        )
        return redirect("carts:cart_detail")
