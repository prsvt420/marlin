from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise


class CatalogConfig(AppConfig):
    """Django application configuration for the Catalog app.

    This class defines the configuration for the `apps.catalog` application.
    """

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "apps.catalog"
    verbose_name: StrOrPromise = _("Catalog")
    label: str = "catalog"
