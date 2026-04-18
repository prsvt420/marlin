from typing import List

from django.urls import URLPattern, path

from apps.favorites import views

app_name: str = "favorites"

urlpatterns: List[URLPattern] = [
    path(route="", view=views.FavoriteListView.as_view(), name="list"),
    path(
        route="<int:product_pk>/toggle/",
        view=views.FavoriteToggleView.as_view(),
        name="toggle",
    ),
]
