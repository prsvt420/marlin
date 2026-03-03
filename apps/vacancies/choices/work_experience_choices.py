from django.db import models
from django.utils.translation import gettext_lazy as _


class WorkExperience(models.TextChoices):
    NO_EXPERIENCE = "no_exp", _("No experience")
    ONE_TO_THREE = "1_3", _("From 1 to 3 years")
    THREE_TO_SIX = "3_6", _("From 3 to 6 years")
    MORE_THAN_SIX = "6_plus", _("More than 6 years")
