from django.db import models
from django.utils.translation import gettext_lazy as _


class UnitType(models.TextChoices):
    """Enumeration for product measurement units.

    Defines the available units of measurement for products.

    Attributes:
        KILOGRAM: Kilogram unit ("kg").
        LITER: Liter unit ("l").
        PIECE: Piece/unit ("pcs").
    """

    KILOGRAM = "kg", _("kg")
    LITER = "l", _("L")
    PIECE = "pcs", _("pcs")
