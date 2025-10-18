from typing import List

from django.urls import URLPattern, path

from . import views

app_name: str = "catalog"

urlpatterns: List[URLPattern] = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path(
        "product/<slug:slug>",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
]
