from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise


class CartsConfig(AppConfig):
    """Django application configuration for the Carts app.

    This class defines the configuration for the `apps.carts` application.
    """

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "apps.carts"
    verbose_name: StrOrPromise = _("Carts")
    label: str = "carts"
