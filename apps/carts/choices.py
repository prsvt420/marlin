from django.db import models
from django.utils.translation import gettext_lazy as _


class CartStatus(models.TextChoices):
    """Enumeration for cart lifecycle states.

    Defines the possible statuses of a cart during its lifecycle.

    Attributes:
            ACTIVE: Cart is active and can be modified.
            CONVERTED: Cart has been converted into an order.
            ABANDONED: Cart was abandoned and is no longer active.
    """

    ACTIVE = "active", _("Active")
    CONVERTED = "converted", _("Сonverted")
    ABANDONED = "abandoned", _("Abandoned")
