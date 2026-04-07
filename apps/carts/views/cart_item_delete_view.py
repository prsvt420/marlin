from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.carts.exceptions import CartItemNotFoundError
from apps.carts.models import Cart
from apps.carts.services import CartService


class CartItemDeleteView(LoginRequiredMixin, View):

    def post(self, request: HttpRequest, cart_item_pk: int) -> HttpResponse:
        cart: Cart = CartService().get_or_create_active_cart_for_user(
            user=self.request.user  # type: ignore
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
        return redirect(to=request.META.get("HTTP_REFERER", "pages:home"))
