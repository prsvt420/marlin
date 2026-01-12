from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuration for the core application."""

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "apps.core"
    label: str = "core"
