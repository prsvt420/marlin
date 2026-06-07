from typing import List

from django.urls import URLPattern, path

from apps.reviews import views

app_name: str = "reviews"

urlpatterns: List[URLPattern] = [
    path(
        route="products/<int:product_pk>/rating/",
        view=views.ProductReviewUpdateView.as_view(),
        name="product-rating-update",
    ),
]
