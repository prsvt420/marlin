from typing import Any, Dict, Optional

from django.db.models import QuerySet
from django.views import generic

from apps.catalog.constants import ORDERING_OPTIONS
from apps.catalog.dataclasses import OrderingOption
from apps.catalog.models import Category, Product
from apps.catalog.repositories.category_repository import CategoryRepository
from apps.catalog.repositories.product_repository import ProductRepository


class CategoryListView(generic.ListView):
    """Displays a list of products in the catalog.

    Uses the `catalog/category_list.html` template and provides
    a context variable `parent_categories` containing all Category objects.
    """

    model = Category
    template_name = "catalog/category_list.html"
    context_object_name = "parent_categories"

    def get_queryset(self) -> QuerySet[Category]:
        """Return the queryset of parent categories.

        Returns:
            QuerySet[Category]: A queryset of parent Category objects.
        """
        return CategoryRepository.get_parents()


class ProductListView(generic.ListView):
    """Displays a list of products in the catalog.

    Uses the `catalog/product_list.html` template and provides
    a context variable `products` containing all Product objects.
    """

    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 12
    paginate_orphans = 4
    extra_context = {"ordering_options": ORDERING_OPTIONS}

    def get_queryset(self) -> QuerySet[Product]:
        """Return the queryset of products.

        Returns:
            QuerySet[Product]: A queryset of Product objects.
        """
        search_query: str = self.search_query
        order_field: Optional[str] = self.ordering_option.field
        category_slug: Optional[str] = self.category_slug

        return ProductRepository.filter(
            search_query=search_query,
            order_field=order_field,
            category_slug=category_slug,
        )

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add additional context variables to the template.

        Args:
            **kwargs: Additional context passed to the base implementation.

        Returns:
            Dict[str, Any]: The context dictionary for the template.
        """
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["search_query"] = self.search_query
        context["current_ordering_option"] = self.ordering_option
        context["category"] = CategoryRepository.get_by_slug(
            slug=self.category_slug
        )
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
    def category_slug(self) -> str:
        """Return the category slug from URL keyword arguments.

        Fetches the 'slug' parameter from `self.kwargs` and returns it.

        Returns:
            str: The category slug string. Returns an empty string if
            no slug parameter is provided in the URL.
        """
        return self.kwargs.get("slug", "")

    @property
    def search_query(self) -> str:
        """Return the search query string from the request.

        Fetches the 'q' GET parameter and strips whitespace from
        the beginning and end.

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
