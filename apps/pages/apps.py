from django.apps import AppConfig


class PagesConfig(AppConfig):
    """Django application configuration for the Pages app.

    This class defines the configuration for the `apps.pages` application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.pages"
    verbose_name: str = "Страницы"
    label: str = "pages"
