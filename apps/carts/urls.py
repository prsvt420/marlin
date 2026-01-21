from typing import List

from django.urls import URLPattern, path  # noqa: F401

from apps.carts import views  # noqa: F401

app_name: str = "carts"

urlpatterns: List[URLPattern] = []
