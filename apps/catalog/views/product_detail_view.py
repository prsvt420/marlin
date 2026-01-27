from django.db.models import QuerySet
from django.views.generic import DetailView

from apps.catalog.models import Product
from apps.catalog.repositories import ProductRepository


class ProductDetailView(DetailView):
    """View for displaying the product detail."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self) -> QuerySet[Product]:
        """Return all active products."""
        return ProductRepository.filter()
