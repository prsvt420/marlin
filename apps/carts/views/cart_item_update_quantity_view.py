import re
from typing import Dict, Optional

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.carts.exceptions import (
    CartItemNotFoundError,
    InsufficientStockError,
    InvalidCartItemQuantityError,
    ProductUnavailableError,
)
from apps.carts.mixins import HtmxLoginRequiredMixin
from apps.carts.models import Cart, CartItem
from apps.carts.selectors import CartSelector
from apps.carts.services import CartService


class CartItemUpdateQuantityView(HtmxLoginRequiredMixin, View):

    def post(  # noqa: C901
        self, request: HttpRequest, cart_item_pk: int
    ) -> HttpResponse:
        action: Optional[str] = request.POST.get(key="action")
        cart: Cart = CartService().get_or_create_active_cart_for_user(
            user=self.request.user  # type: ignore
        )

        actions: Dict[Optional[str], int] = {"increment": 1, "decrement": -1}
        delta: Optional[int] = actions.get(action)

        if delta is None:
            messages.error(
                request,
                _(
                    "An error occurred while changing the quantity of the "
                    "product in the cart. An invalid action is specified."
                ),
            )
            return redirect(to="carts:detail")

        try:
            CartService().adjust_cart_item_quantity(
                cart=cart, cart_item_pk=cart_item_pk, delta=delta
            )
        except InvalidCartItemQuantityError:
            messages.error(
                request,
                _(
                    "An error occurred while changing the quantity of the "
                    "product in the cart. The quantity specified is incorrect."
                ),
            )
        except CartItemNotFoundError:
            messages.error(
                request,
                _(
                    "An error occurred while changing the quantity of the "
                    "product in the cart. The product is not in the cart."
                ),
            )
        except ProductUnavailableError:
            messages.error(
                request,
                _(
                    "An error occurred while changing the quantity of the "
                    "product in the cart. Product is unavailable."
                ),
            )
        except InsufficientStockError:
            messages.error(
                request,
                _(
                    "An error occurred while changing the quantity of the "
                    "product in the cart. The requested quantity "
                    "is out of stock."
                ),
            )
        except Exception:
            messages.error(
                request,
                _(
                    "An error occurred while changing the quantity of the "
                    "product in the cart. Please try again."
                ),
            )
        else:
            messages.success(
                request,
                _(
                    "The quantity of the product in the cart has been "
                    "successfully updated. The price has been updated."
                ),
            )

        if request.htmx:  # type: ignore
            cart_item: Optional[CartItem] = CartSelector().get_cart_item(
                cart=cart, cart_item_pk=cart_item_pk
            )

            htmx_target: Optional[str] = request.htmx.target  # type: ignore

            if htmx_target and re.match(
                pattern=r"^cart-item-control-\d+$", string=htmx_target
            ):
                if cart_item:
                    return render(
                        request,
                        template_name=(
                            "carts/includes/_cart_item_control_htmx.html"
                        ),
                        context={"cart_item": cart_item},
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
