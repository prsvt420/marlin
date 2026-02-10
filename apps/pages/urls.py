from typing import List

from django.urls import URLPattern, path
from django.views.generic import RedirectView, TemplateView

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
        view=TemplateView.as_view(template_name="pages/privacy.html"),
        name="privacy",
    ),
    path(
        route="terms/",
        view=TemplateView.as_view(template_name="pages/terms.html"),
        name="terms",
    ),
    path(
        route="offer/",
        view=TemplateView.as_view(template_name="pages/offer.html"),
        name="offer",
    ),
]
