from typing import Any, Dict, Optional

from django.db.models import QuerySet
from django.views import generic

from apps.catalog.constants import ORDERING_OPTIONS
from apps.catalog.dataclasses import OrderingOption
from apps.catalog.models import Product
from apps.catalog.repositories.product_repository import ProductRepository


class ProductListView(generic.ListView):
    """Displays a list of products in the catalog.

    Uses the `catalog/product_list.html` template and provides
    a context variable `products` containing all Product objects.
    Optionally filtered by search query.
    """

    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 12
    paginate_orphans = 4
    extra_context = {"ordering_options": ORDERING_OPTIONS}

    def get_queryset(self) -> QuerySet[Product]:
        """Return the queryset of products.

        If the `q` GET parameter is provided, the queryset is filtered
        based on the search query.

        Returns:
            QuerySet[Product]: A queryset of Product objects,
            optionally filtered by the search term.
        """
        search_query: str = self.search_query

        order_field: Optional[str] = self.ordering_option.field

        return ProductRepository.filter(
            search_query=search_query,
            order_field=order_field,
        )

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
        context["search_query"] = self.search_query
        context["current_ordering_option"] = self.ordering_option
        return context

    @property
    def ordering_option(self) -> OrderingOption:
        """Return the currently selected product ordering option.

        Fetches the 'sort' GET parameter from the request and returns
        the corresponding `OrderingOption` from `ORDERING_OPTIONS`.

        Returns:
            OrderingOption: The selected ordering option.
        """
        ordering_option_key: str = self.request.GET.get("sort", "").strip()
        return ORDERING_OPTIONS.get(ordering_option_key, ORDERING_OPTIONS[""])

    @property
    def search_query(self) -> str:
        """Return the search query string from the request.

        Fetches the 'q' GET parameter and strips whitespace from
        the beginning and end. Used to filter the product queryset.

        Returns:
            str: The cleaned search query string. Returns an empty
            string if no query parameter is provided.
        """
        return self.request.GET.get("q", "").strip()


class ProductDetailView(generic.DetailView):
    """Displays detailed information about a specific product.

    Uses the `catalog/product_detail.html` template and provides
    a context variable `product` containing the selected Product object.
    """

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self) -> QuerySet[Product]:
        """Return the queryset of products.

        Returns:
            QuerySet[Product]: A queryset of Product objects.
        """
        return ProductRepository.filter()
