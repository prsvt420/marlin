from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.carts.models import Cart
from apps.carts.services import CartService
from apps.core.mixins import HtmxLoginRequiredMixin


class CartClearView(HtmxLoginRequiredMixin, View):

    def post(self, request: HttpRequest) -> HttpResponse:
        cart: Cart = CartService().get_or_create_active_cart_for_user(
            user=self.request.user  # type: ignore
        )
        CartService().clear_cart(cart=cart)
        messages.success(
            request,
            _("Your cart has been successfully cleared."),
        )
        if request.htmx:  # type: ignore
            return render(
                request,
                template_name="carts/includes/_cart_clear_htmx.html",
            )
        return redirect(to="carts:detail")
