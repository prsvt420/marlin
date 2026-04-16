from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise


class FavoritesConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "apps.favorites"
    verbose_name: StrOrPromise = _("Favorites")
    label: str = "favorites"
