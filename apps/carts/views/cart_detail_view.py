from typing import Optional

from django.contrib import messages
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView

from apps.carts.models import Cart
from apps.carts.selectors import CartSelector
from apps.carts.services import CartService
from apps.core.mixins import HtmxLoginRequiredMixin


class CartDetailView(HtmxLoginRequiredMixin, DetailView):
    template_name = "carts/cart_detail.html"
    context_object_name = "cart"
    extra_context = {
        "breadcrumbs": [
            {"name": _("Home"), "url": reverse_lazy(viewname="pages:home")},
            {
                "name": _("Cart"),
                "url": reverse_lazy(viewname="carts:detail"),
            },
        ]
    }

    def get_object(self, queryset: Optional[QuerySet[Cart]] = None) -> Cart:
        cart: Cart = CartService().get_or_create_active_cart_for_user(
            user=self.request.user  # type: ignore
        )

        if CartSelector().has_unavailable_cart_items(cart=cart):
            messages.warning(
                self.request,
                _(
                    "There are unavailable products in your cart. "
                    "Please delete them."
                ),
            )

        if CartService().validate_cart_item_quantities(cart=cart):
            messages.warning(
                self.request,
                _(
                    "The stock availability has changed. "
                    "The price has been updated."
                ),
            )

        return cart
