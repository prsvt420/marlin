from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PagesConfig(AppConfig):
    """Django application configuration for the Pages app.

    This class defines the configuration for the `apps.pages` application.
    """

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "apps.pages"
    verbose_name = _("Pages")
    label: str = "pages"
