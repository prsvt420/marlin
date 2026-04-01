from typing import List

from django.urls import URLPattern, path

from apps.catalog import views

app_name: str = "catalog"

urlpatterns: List[URLPattern] = [
    path(
        route="", view=views.CategoryListView.as_view(), name="category-list"
    ),
    path(
        route="search/",
        view=views.ProductSearchListView.as_view(),
        name="product-search-list",
    ),
    path(
        route="<slug:category_slug>/",
        view=views.ProductListView.as_view(),
        name="product-list",
    ),
    path(
        route="<slug:category_slug>/p/<slug:product_slug>/",
        view=views.ProductDetailView.as_view(),
        name="product-detail",
    ),
]
