from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBase,
)
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from apps.carts.models import Cart
from apps.carts.selectors import CartSelector
from apps.carts.services import CartService
from apps.orders.exceptions import OrderError
from apps.orders.forms import CheckoutForm
from apps.orders.services import OrderService


class CheckoutView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "orders/checkout.html"
    form_class = CheckoutForm
    extra_context = {
        "breadcrumbs": [
            {"name": _("Home"), "url": reverse_lazy(viewname="pages:home")},
            {"name": _("Cart"), "url": reverse_lazy(viewname="carts:detail")},
            {
                "name": _("Checkout"),
                "url": reverse_lazy(viewname="orders:checkout"),
            },
        ],
    }
    success_message = _("The order has been successfully created.")

    @property
    def cart(self) -> Cart:
        return CartService().get_or_create_active_cart_for_user(
            user=self.request.user  # type: ignore
        )

    def dispatch(
        self, request: HttpRequest, **kwargs: Any
    ) -> HttpResponseBase:
        if CartSelector().is_cart_empty(cart=self.cart):
            messages.info(request, _("Your cart is empty."))
            return redirect(to="carts:detail")

        if CartSelector().has_unavailable_cart_items(cart=self.cart):
            return redirect(to="carts:detail")

        return super().dispatch(request=request, **kwargs)

    def form_valid(self, form: CheckoutForm) -> HttpResponse:
        try:
            OrderService().checkout(
                user=self.request.user,  # type: ignore
                cart=self.cart,
                **form.cleaned_data,
            )
        except OrderError:
            messages.error(
                self.request, _("An error occurred while creating the order.")
            )
            return redirect(to="carts:detail")

        return super().form_valid(form=form)

    def form_invalid(self, form: CheckoutForm) -> HttpResponse:
        messages.error(
            self.request,
            _("Please correct the errors in the form and try again."),
        )
        return super().form_invalid(form=form)

    def get_success_url(self) -> str:
        return reverse(viewname="catalog:category-list")
