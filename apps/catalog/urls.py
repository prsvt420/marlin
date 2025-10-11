from typing import List

from django.urls import URLPattern, path  # noqa: F401

from . import views  # noqa: F401

app_name: str = "catalog"

urlpatterns: List[URLPattern] = []
