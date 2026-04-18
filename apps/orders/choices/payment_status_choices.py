from django.db import models
from django.utils.translation import pgettext_lazy


class PaymentStatus(models.TextChoices):
    PENDING = "pending", pgettext_lazy("feminine", "Pending")
    PAID = "paid", pgettext_lazy("feminine", "Paid")
    FAILED = "failed", pgettext_lazy("feminine", "Failed")
    REFUNDED = "refunded", pgettext_lazy("feminine", "Refunded")
