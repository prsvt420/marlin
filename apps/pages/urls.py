from typing import List

from django.urls import URLPattern, path

from . import views

app_name: str = "pages"

urlpatterns: List[URLPattern] = [
    path("contact", views.ContactView.as_view(), name="contact")
]
