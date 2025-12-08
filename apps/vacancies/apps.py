from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise


class VacanciesConfig(AppConfig):
    """Django application configuration for the Vacancies app.

    This class defines the configuration for the `apps.vacancies` application.
    """

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "apps.vacancies"
    verbose_name: StrOrPromise = _("Vacancies")
    label: str = "vacancies"
