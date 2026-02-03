from typing import Any, Dict

from django.db.models import QuerySet
from django.views.generic import DetailView

from apps.carts.repositories import CartRepository
from apps.catalog.models import Product
from apps.catalog.repositories import ProductRepository


class ProductDetailView(DetailView):
    """View for displaying the product detail."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self) -> QuerySet[Product]:
        """Return all active products."""
        return ProductRepository().get_filtered()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add additional context variables to the template."""
        context_data: Dict[str, Any] = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context_data["existing_products"] = (
                CartRepository.get_existing_products(self.request.user)
            )

        return context_data
