from django.db import models
from django.utils.translation import gettext_lazy as _


class UnitType(models.TextChoices):
    """Text choices for specifying the unit of measurement."""

    KILOGRAM = "kg", _("kg")
    LITER = "l", _("L")
    PIECE = "pcs", _("pcs")
