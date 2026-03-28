from typing import List

from django.urls import URLPattern, path
from django.views.generic import RedirectView

from apps.pages import views

app_name: str = "pages"

urlpatterns: List[URLPattern] = [
    path(
        route="",
        view=RedirectView.as_view(pattern_name="catalog:category-list"),
        name="home",
    ),
    path(route="contact/", view=views.ContactView.as_view(), name="contact"),
    path(
        route="privacy/",
        view=views.PrivacyView.as_view(),
        name="privacy",
    ),
    path(
        route="terms/",
        view=views.TermsView.as_view(),
        name="terms",
    ),
    path(
        route="offer/",
        view=views.OfferView.as_view(),
        name="offer",
    ),
]
