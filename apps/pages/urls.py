from typing import List

from django.urls import URLPattern, path

from . import views

app_name: str = "pages"

urlpatterns: List[URLPattern] = [
    path("", views.CatalogRedirectView.as_view(), name="home"),
    path("contact", views.ContactView.as_view(), name="contact"),
    path("privacy", views.PrivacyView.as_view(), name="privacy"),
    path("terms", views.TermsView.as_view(), name="terms"),
    path("offer", views.OfferView.as_view(), name="offer"),
]
