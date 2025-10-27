from django.apps import AppConfig


class VacanciesConfig(AppConfig):
    """Django application configuration for the Vacancies app.

    This class defines the configuration for the `apps.vacancies` application.
    """

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "apps.vacancies"
    verbose_name: str = "Вакансии"
    label: str = "vacancies"
