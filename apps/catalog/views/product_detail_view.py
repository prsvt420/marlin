from django.db.models import QuerySet
from django.views import generic

from apps.catalog.models import Product
from apps.catalog.repositories import ProductRepository


class ProductDetailView(generic.DetailView):
    """View for displaying the product detail."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self) -> QuerySet[Product]:
        """Return all active products."""
        return ProductRepository.filter()
