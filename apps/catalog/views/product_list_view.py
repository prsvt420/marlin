from typing import Any, Dict, Optional

from django.db.models import QuerySet
from django.views import generic

from apps.catalog.constants import ORDERING_OPTIONS
from apps.catalog.dataclasses import OrderingOption
from apps.catalog.models import Product
from apps.catalog.repositories import CategoryRepository, ProductRepository


class ProductListView(generic.ListView):
    """View for displaying the product list."""

    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 12
    paginate_orphans = 4
    extra_context = {"ordering_options": ORDERING_OPTIONS}

    def get_queryset(self) -> QuerySet[Product]:
        """Return filtered products."""
        search_query: str = self.search_query
        order_field: Optional[str] = self.ordering_option.field
        category_slug: Optional[str] = self.category_slug

        return ProductRepository.filter(
            search_query=search_query,
            order_field=order_field,
            category_slug=category_slug,
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add additional context variables to the template."""
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["search_query"] = self.search_query
        context["current_ordering_option"] = self.ordering_option
        context["category"] = CategoryRepository.get_by_slug(
            slug=self.category_slug
        )
        return context

    @property
    def ordering_option(self) -> OrderingOption:
        """Return the current ordering option from GET parameters."""
        ordering_option_key: str = self.request.GET.get("sort", "").strip()
        return ORDERING_OPTIONS.get(ordering_option_key, ORDERING_OPTIONS[""])

    @property
    def category_slug(self) -> str:
        """Return the current category slug from URL keyword arguments."""
        return self.kwargs.get("slug", "")

    @property
    def search_query(self) -> str:
        """Return the current search query from GET parameters."""
        return self.request.GET.get("q", "").strip()
