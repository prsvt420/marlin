from typing import List

from django.urls import URLPattern, path

from apps.carts import views

app_name: str = "carts"

urlpatterns: List[URLPattern] = [
    path("", views.CartDetailView.as_view(), name="cart_detail"),
    path("clear", views.CartClearView.as_view(), name="cart_clear"),
    path(
        "items/<slug:product_slug>/delete",
        views.CartItemDeleteView.as_view(),
        name="cart_item_delete",
    ),
    path(
        "items/<slug:product_slug>/create",
        views.CartItemCreateView.as_view(),
        name="cart_item_create",
    ),
    path(
        "items/<slug:product_slug>/decrement",
        views.CartItemQuantityDecrementView.as_view(),
        name="cart_item_decrement",
    ),
    path(
        "items/<slug:product_slug>/increment",
        views.CartItemQuantityIncrementView.as_view(),
        name="cart_item_increment",
    ),
]
