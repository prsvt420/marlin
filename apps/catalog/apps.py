from django.apps import AppConfig


class CatalogConfig(AppConfig):
    """Django application configuration for the Catalog app.

    This class defines the configuration for the `apps.catalog` application.
    """

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "apps.catalog"
    verbose_name: str = "Catalog"
    label: str = "catalog"
