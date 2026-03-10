from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name: str = "apps.orders"
    verbose_name: StrOrPromise = _("Orders")
    label: str = "orders"
