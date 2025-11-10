from django.db import models
from django.utils.translation import gettext_lazy as _


class UnitType(models.TextChoices):
    """Enumeration for product measurement units.

    Defines the available units of measurement for products.
    Can be used as choices for the `unit_type` field in Product.

    Attributes:
        KILOGRAM (str): Kilogram unit ("kg").
        LITER (str): Liter unit ("l").
        PIECE (str): Piece/unit ("pcs").
    """

    KILOGRAM = "kg", _("kg")
    LITER = "l", _("L")
    PIECE = "pcs", _("pcs")
