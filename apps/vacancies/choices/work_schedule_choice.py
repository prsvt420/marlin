from django.db import models
from django.utils.translation import gettext_lazy as _


class WorkSchedule(models.TextChoices):
    """Text choices for specifying the type of work schedule."""

    FULL_TIME = "full", _("Full-time")
    SHIFT = "shift", _("Shift schedule")
    FLEXIBLE = "flex", _("Flexible schedule")
    REMOTE = "remote", _("Remote work")
