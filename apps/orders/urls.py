from typing import List

from django.urls import URLPattern, path

from apps.orders import views

app_name: str = "orders"

urlpatterns: List[URLPattern] = [
    path(
        route="checkout/", view=views.CheckoutView.as_view(), name="checkout"
    ),
    path(
        route="<str:order_number>/",
        view=views.OrderDetailView.as_view(),
        name="detail",
    ),
]
