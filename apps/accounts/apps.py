from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountsConfig(AppConfig):
    """Django application configuration for the Accounts app.

    This class defines the configuration for the `apps.accounts` application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    verbose_name = _("Accounts")
    label: str = "accounts"
