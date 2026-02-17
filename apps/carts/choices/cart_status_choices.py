from django.db import models
from django.utils.translation import gettext_lazy as _


class CartStatus(models.TextChoices):
    ACTIVE = "active", _("Active")
    CONVERTED = "converted", _("Сonverted")
    ABANDONED = "abandoned", _("Abandoned")
