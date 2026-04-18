from django.db import models
from django.utils.translation import gettext_lazy as _


class DeliveryMethod(models.TextChoices):
    COURIER = "courier", _("Courier")
    PICKUP = "pickup", _("Pickup")
