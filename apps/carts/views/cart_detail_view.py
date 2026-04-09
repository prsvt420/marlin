from typing import Any, Dict, Optional

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView

from apps.carts.models import Cart
from apps.carts.selectors import CartSelector
from apps.carts.services import CartService


class CartDetailView(LoginRequiredMixin, DetailView):
    template_name = "carts/redesign/cart_detail.html"
    context_object_name = "cart"

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

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["cart_prices"] = CartSelector().get_cart_prices(
            cart=self.object
        )
        context["available_cart_items"] = (
            CartSelector().get_available_cart_items(cart=self.object)
        )
        context["unavailable_cart_items"] = (
            CartSelector().get_unavailable_cart_items(cart=self.object)
        )
        context["breadcrumbs"] = [
            {"name": _("Home"), "url": reverse_lazy(viewname="pages:home")},
            {
                "name": _("Cart"),
                "url": reverse_lazy(viewname="carts:detail"),
            },
        ]
        return context
