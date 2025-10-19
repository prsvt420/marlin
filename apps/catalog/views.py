from typing import Any, Dict

from django.db.models import QuerySet
from django.views import generic

from apps.catalog.models import Product
from apps.catalog.repositories.product_repository import ProductRepository


class ProductListView(generic.ListView):
    """Displays a list of products in the catalog.

    Uses the 'catalog/product_list.html' template and provides
    a context variable 'products' containing all Product objects.
    Optionally filtered by search query.
    """

    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 12
    paginate_orphans = 4

    def get_queryset(self) -> QuerySet[Product]:
        """Return the queryset of products.

        If the "q" GET parameter is provided, the queryset is filtered
        by product names containing the query substring (case-insensitive).

        Returns:
            QuerySet[Product]: A queryset of Product objects,
            optionally filtered by the search term.
        """
        search_query: str = self.request.GET.get("q", "").strip()

        if search_query:
            return ProductRepository.find_by_search_query(
                search_query=search_query
            )

        return ProductRepository.find_active()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add additional context variables to the template.

        Adds the current search query (if any) to the context
        under the key `search_query` to preserve the input in the search field.

        Args:
            **kwargs: Additional context passed to the base implementation.

        Returns:
            Dict[str, Any]: The context dictionary for the template.
        """
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        return context


class ProductDetailView(generic.DetailView):
    """Displays detailed information about a specific product.

    Uses the 'catalog/product_detail.html' template and provides
    a context variable 'product' containing the selected Product object.
    """

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self) -> QuerySet[Product]:
        """Return the queryset of products.

        Returns:
            QuerySet[Product]: A queryset of Product objects.
        """
        return ProductRepository.find_active()
