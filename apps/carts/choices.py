from django.db import models
from django.utils.translation import gettext_lazy as _


class CartStatus(models.TextChoices):
    """Text choices for indicating the current status of a shopping cart."""

    ACTIVE = "active", _("Active")
    CONVERTED = "converted", _("Сonverted")
    ABANDONED = "abandoned", _("Abandoned")
