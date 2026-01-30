from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.carts.repositories import CartRepository


class CartClearView(LoginRequiredMixin, View):
    """View for clearing the cart."""

    def post(self, request: HttpRequest) -> HttpResponse:
        """Clear the user active cart and redirect to cart detail."""
        CartRepository.clear_cart(request.user)  # type: ignore
        messages.success(
            request,
            _("Your cart has been successfully cleared."),
        )
        return redirect("carts:cart_detail")
