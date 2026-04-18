from django.db import models
from django.utils.translation import pgettext_lazy


class OrderStatus(models.TextChoices):
    PENDING = "pending", pgettext_lazy("masculine", "Pending")
    CONFIRMED = "confirmed", pgettext_lazy("masculine", "Confirmed")
    ASSEMBLING = "assembling", pgettext_lazy("masculine", "Assembling")
    SHIPPED = "shipped", pgettext_lazy("masculine", "Shipped")
    COMPLETED = "completed", pgettext_lazy("masculine", "Completed")
    CANCELLED = "cancelled", pgettext_lazy("masculine", "Cancelled")
