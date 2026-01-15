from django.views.generic import RedirectView


class CatalogRedirectView(RedirectView):
    """View for redirecting to the category list."""

    pattern_name = "catalog:category_list"
    permanent = True
