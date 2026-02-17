from typing import List

from django.urls import URLPattern, path

from apps.carts import views

app_name: str = "carts"

urlpatterns: List[URLPattern] = [
    path("", views.CartDetailView.as_view(), name="detail"),
    path("clear/", views.CartClearView.as_view(), name="clear"),
    path(
        "items/<int:cart_item_pk>/delete/",
        views.CartItemDeleteView.as_view(),
        name="cart-item-delete",
    ),
    path(
        "items/<int:product_pk>/create/",
        views.CartItemCreateView.as_view(),
        name="cart-item-create",
    ),
    path(
        "items/<int:cart_item_pk>/update-quantity/",
        views.CartItemUpdateQuantityView.as_view(),
        name="cart-item-update-quantity",
    ),
]
