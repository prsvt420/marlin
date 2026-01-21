from typing import List

from django.urls import URLPattern, path  # noqa: F401

from apps.promotions import views  # noqa: F401

app_name: str = "promotions"

urlpatterns: List[URLPattern] = []
