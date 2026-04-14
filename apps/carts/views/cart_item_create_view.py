from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.carts.exceptions import (
    CartItemAlreadyExistsError,
    InsufficientStockError,
    InvalidCartItemQuantityError,
    ProductUnavailableError,
)
from apps.carts.mixins import HtmxLoginRequiredMixin
from apps.carts.models import Cart
from apps.carts.services import CartService
from apps.catalog.selectors import ProductSelector


class CartItemCreateView(HtmxLoginRequiredMixin, View):

    def post(self, request: HttpRequest, product_pk: int) -> HttpResponse:
        cart: Cart = CartService().get_or_create_active_cart_for_user(
            user=self.request.user  # type: ignore
        )

        try:
            CartService().create_cart_item(
                cart=cart,
                product_pk=product_pk,
            )
        except InvalidCartItemQuantityError:
            messages.error(
                request,
                _(
                    "An error occurred while adding the product to the cart. "
                    "The quantity specified is incorrect."
                ),
            )
        except ProductUnavailableError:
            messages.error(
                request,
                _(
                    "An error occurred while adding the product to the cart. "
                    "Product is unavailable."
                ),
            )
        except InsufficientStockError:
            messages.error(
                request,
                _(
                    "An error occurred while adding the product to the cart. "
                    "The requested quantity is out of stock."
                ),
            )
        except CartItemAlreadyExistsError:
            messages.error(
                request,
                _(
                    "An error occurred while adding the product to the cart. "
                    "The product is already in the cart."
                ),
            )
        except Exception:
            messages.error(
                request,
                _(
                    "An error occurred while adding the product to the cart. "
                    "Please try again."
                ),
            )
        else:
            messages.success(
                request,
                _(
                    "The product has been successfully added to your cart. "
                    "The price has been updated."
                ),
            )

        if request.htmx:  # type: ignore
            return render(
                request,
                template_name=(
                    "carts/redesign/includes/"
                    "_product_cart_item_control_htmx.html"
                ),
                context={
                    "product": ProductSelector().get_product(
                        product_pk=product_pk
                    ),
                },
            )

        return redirect(to=request.META.get("HTTP_REFERER", "pages:home"))
