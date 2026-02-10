from typing import List, Union

from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path

urlpatterns: List[Union[URLResolver, URLPattern]] = [
    path(
        route="admin/doc/", view=include(arg="django.contrib.admindocs.urls")
    ),
    path(route="admin/", view=admin.site.urls),
    path(route="i18n/", view=include(arg="django.conf.urls.i18n")),
    path(
        route="catalog/",
        view=include(arg="apps.catalog.urls", namespace="catalog"),
    ),
    path(
        route="",
        view=include(arg="apps.pages.urls", namespace="pages"),
    ),
    path(
        route="vacancies/",
        view=include(arg="apps.vacancies.urls", namespace="vacancies"),
    ),
    path(
        route="accounts/",
        view=include(arg="apps.accounts.urls", namespace="accounts"),
    ),
    path(
        route="carts/",
        view=include(arg="apps.carts.urls", namespace="carts"),
    ),
    path(
        route="promotions/",
        view=include(arg="apps.promotions.urls", namespace="promotions"),
    ),
]


if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(
        prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
