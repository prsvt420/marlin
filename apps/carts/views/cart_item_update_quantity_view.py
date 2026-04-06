from typing import Dict, Optional

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.carts.exceptions import (
    CartItemNotFoundError,
    InsufficientStockError,
    InvalidCartItemQuantityError,
    ProductUnavailableError,
)
from apps.carts.models import Cart
from apps.carts.services import CartService


class CartItemUpdateQuantityView(LoginRequiredMixin, View):

    def post(self, request: HttpRequest, cart_item_pk: int) -> HttpResponse:
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
        return redirect(to=request.META.get("HTTP_REFERER", "pages:home"))
