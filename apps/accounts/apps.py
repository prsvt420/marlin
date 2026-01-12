from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise


class AccountsConfig(AppConfig):
    """Configuration for the accounts application."""

    default_auto_field = "django.db.models.BigAutoField"
    name: str = "apps.accounts"
    verbose_name: StrOrPromise = _("Accounts")
    label: str = "accounts"
