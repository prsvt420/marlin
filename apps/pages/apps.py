from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise


class PagesConfig(AppConfig):
    """Django application configuration for the Pages app.

    This class defines the configuration for the `apps.pages` application.
    """

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "apps.pages"
    verbose_name: StrOrPromise = _("Pages")
    label: str = "pages"
