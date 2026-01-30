from typing import Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import DetailView

from apps.carts.models import Cart
from apps.carts.repositories import CartRepository


class CartDetailView(LoginRequiredMixin, DetailView):
    """View for displaying the cart detail."""

    model = Cart
    template_name = "carts/cart_detail.html"
    context_object_name = "cart"

    def get_object(self, queryset: Optional[QuerySet] = None) -> Cart:
        """Return the user active cart."""
        return CartRepository.get_user_active_cart(
            user=self.request.user  # type: ignore
        )
