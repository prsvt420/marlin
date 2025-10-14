from django.views import generic

from apps.catalog.models import Product


class ProductListView(generic.ListView):
    """Displays a list of products in the catalog.

    Uses the 'catalog/product_list.html' template and provides
    a context variable 'products' containing all Product objects.
    """

    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
