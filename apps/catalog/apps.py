from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise


class CatalogConfig(AppConfig):

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "apps.catalog"
    verbose_name: StrOrPromise = _("Catalog")
    label: str = "catalog"
