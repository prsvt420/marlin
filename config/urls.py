from typing import List, Union

from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path
from django.views.generic import TemplateView
from health_check.views import HealthCheckView
from redis.asyncio import Redis as RedisClient

handler403: str = "apps.core.views.handler403"

urlpatterns: List[Union[URLResolver, URLPattern]] = [
    path(
        route="admin/doc/", view=include(arg="django.contrib.admindocs.urls")
    ),
    path(route="admin/", view=admin.site.urls),
    path(route="i18n/", view=include(arg="django.conf.urls.i18n")),
    path(
        route="health/0qG5wX8gC-XJzAqi4WvSD3mXQmae_NFP1XoWWd_6Bwg/",
        view=HealthCheckView.as_view(
            checks=[
                "health_check.Cache",
                "health_check.Database",
                "health_check.Mail",
                "health_check.Storage",
                "health_check.contrib.celery.Ping",
                "health_check.contrib.psutil.Disk",
                "health_check.contrib.psutil.Memory",
                "health_check.contrib.psutil.CPU",
                (
                    "health_check.contrib.redis.Redis",
                    {
                        "client": RedisClient.from_url(
                            url="redis://localhost:6379"
                        )
                    },
                ),
            ],
        ),
        name="health-check",
    ),
    path(
        route="catalog/",
        view=include(arg="apps.catalog.urls", namespace="catalog"),
    ),
    path(
        route="",
        view=include(arg="apps.pages.urls", namespace="pages"),
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
    path(
        route="orders/",
        view=include(arg="apps.orders.urls", namespace="orders"),
    ),
    path(
        route="reviews/",
        view=include(arg="apps.reviews.urls", namespace="reviews"),
    ),
    path(
        route="favorites/",
        view=include(arg="apps.favorites.urls", namespace="favorites"),
    ),
]


if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(
        prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += (
        path(
            route="404/",
            view=TemplateView.as_view(template_name="404.html"),
        ),
        path(
            route="403/",
            view=TemplateView.as_view(template_name="403.html"),
        ),
        path(
            route="429/",
            view=TemplateView.as_view(template_name="429.html"),
        ),
        path(
            route="500/",
            view=TemplateView.as_view(template_name="500.html"),
        ),
        path(
            route="base/",
            view=TemplateView.as_view(template_name="base.html"),
        ),
    )
