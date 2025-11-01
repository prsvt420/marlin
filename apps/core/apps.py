from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Django application configuration for the Core app.

    This class defines the configuration for the `apps.core` application.
    """

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "apps.core"
    label: str = "core"
