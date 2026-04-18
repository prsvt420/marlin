from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentMethod(models.TextChoices):
    ONLINE = "online", _("Online")
    ON_DELIVERY = "on_delivery", _("On delivery")
