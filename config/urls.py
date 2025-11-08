from typing import List, Union

from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path

urlpatterns: List[Union[URLResolver, URLPattern]] = [
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path(
        "catalog/",
        include("apps.catalog.urls", namespace="catalog"),
        name="catalog",
    ),
    path(
        "",
        include("apps.pages.urls", namespace="pages"),
        name="pages",
    ),
    path(
        "vacancies/",
        include("apps.vacancies.urls", namespace="vacancies"),
        name="vacancies",
    ),
    path(
        "accounts/",
        include("apps.accounts.urls", namespace="accounts"),
        name="accounts",
    ),
]


if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
