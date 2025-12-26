from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise


class PromotionsConfig(AppConfig):
    """Django application configuration for the Promotions app.

    This class defines the configuration for the `apps.promotions` application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name: str = "apps.promotions"
    verbose_name: StrOrPromise = _("Promotions")
    label: str = "promotions"
