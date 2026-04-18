import re
from typing import Optional

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.carts.exceptions import CartItemNotFoundError
from apps.carts.models import Cart, CartItem
from apps.carts.selectors import CartSelector
from apps.carts.services import CartService
from apps.core.mixins import HtmxLoginRequiredMixin


class CartItemDeleteView(HtmxLoginRequiredMixin, View):

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
            htmx_target: Optional[str] = request.htmx.target  # type: ignore

            if htmx_target and re.match(
                pattern=r"^cart-item-\d+$", string=htmx_target
            ):
                if cart_item:
                    return render(
                        request,
                        template_name=(
                            "carts/includes/_cart_item_delete_htmx.html"
                        ),
                    )
                return render(
                    request,
                    template_name="carts/includes/_cart_item_stale_htmx.html",
                    context={"cart_item_pk": cart_item_pk},
                )

            return render(
                request,
                template_name=(
                    "carts/includes/_product_cart_item_control_htmx.html"
                ),
                context={
                    "product": cart_item.product if cart_item else None,
                },
            )

        return redirect(to=request.META.get("HTTP_REFERER", "pages:home"))
