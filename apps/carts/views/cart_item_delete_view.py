from typing import Optional

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.carts.exceptions import CartItemNotFoundError
from apps.carts.models import Cart, CartItem
from apps.carts.selectors import CartSelector
from apps.carts.services import CartService


class CartItemDeleteView(LoginRequiredMixin, View):

    def post(self, request: HttpRequest, cart_item_pk: int) -> HttpResponse:
        cart: Cart = CartService().get_or_create_active_cart_for_user(
            user=self.request.user  # type: ignore
        )
        cart_item: Optional[CartItem] = CartSelector().get_cart_item(
            cart=cart, cart_item_pk=cart_item_pk
        )

        try:
            CartService().delete_cart_item(
                cart=cart, cart_item_pk=cart_item_pk
            )
        except CartItemNotFoundError:
            messages.error(
                request,
                _(
                    "An error occurred while deleting the "
                    "product to the cart. The product is not in the cart."
                ),
            )
        except Exception:
            messages.error(
                request,
                _(
                    "An error occurred while deleting the "
                    "product to the cart. Please try again."
                ),
            )
        else:
            messages.success(
                request,
                _(
                    "The product has been successfully deleted from the cart. "
                    "The price has been updated."
                ),
            )

        if request.htmx:  # type: ignore
            return render(
                request,
                template_name=(
                    "carts/redesign/includes/_product_cart_item_control.html"
                ),
                context={
                    "product": cart_item.product if cart_item else None,
                },
            )

        return redirect(to=request.META.get("HTTP_REFERER", "pages:home"))
