from django.db import models
from django.utils.translation import gettext_lazy as _


class UnitType(models.TextChoices):

    KILOGRAM = "kg", _("kg")
    LITER = "l", _("L")
    PIECE = "pcs", _("pcs")
