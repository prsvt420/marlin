from typing import List

from django.urls import URLPattern, path

from apps.carts import views

app_name: str = "carts"

urlpatterns: List[URLPattern] = [
    path("", views.CartDetailView.as_view(), name="cart_detail"),
    path("clear", views.CartClearView.as_view(), name="cart_clear"),
    path(
        "item/delete/<slug:product_slug>",
        views.CartItemDeleteView.as_view(),
        name="cart_item_delete",
    ),
]
