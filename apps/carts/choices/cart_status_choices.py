from django.db import models
from django.utils.translation import pgettext_lazy


class CartStatus(models.TextChoices):
    ACTIVE = "active", pgettext_lazy("feminine", "Active")
    CONVERTED = "converted", pgettext_lazy("feminine", "Сonverted")
    ABANDONED = "abandoned", pgettext_lazy("feminine", "Abandoned")
