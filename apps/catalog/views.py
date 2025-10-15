from typing import Any, Dict

from django.db.models import QuerySet
from django.views import generic

from apps.catalog.models import Product


class ProductListView(generic.ListView):
    """Displays a list of products in the catalog.

    Uses the 'catalog/product_list.html' template and provides
    a context variable 'products' containing all Product objects.
    Optionally filtered by search query.
    """

    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"

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
            return Product.objects.filter(name__icontains=search_query)

        return super().get_queryset()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add additional context variables to the template.

        Adds the current search query (if any) to the context
        under the key ``query`` to preserve the input in the search field.

        Args:
            **kwargs: Additional context passed to the base implementation.

        Returns:
            Dict[str, Any]: The context dictionary for the template.
        """
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        return context
