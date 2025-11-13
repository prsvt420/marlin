from django.db import models
from django.utils.translation import gettext_lazy as _


class ExperienceLevel(models.TextChoices):
    """Enumeration for work experience levels.

    Defines the possible ranges of professional experience
    that can be associated with a job or candidate.

    Attributes:
        NO_EXPERIENCE (str): No prior work experience.
        ONE_TO_THREE (str): From 1 to 3 years of experience.
        THREE_TO_SIX (str): From 3 to 6 years of experience.
        MORE_THAN_SIX (str): More than 6 years of experience.
    """

    NO_EXPERIENCE = "no_exp", _("No experience")
    ONE_TO_THREE = "1_3", _("From 1 to 3 years")
    THREE_TO_SIX = "3_6", _("From 3 to 6 years")
    MORE_THAN_SIX = "6_plus", _("More than 6 years")


class WorkSchedule(models.TextChoices):
    """Enumeration for work schedule types.

    Defines the available types of work schedules
    that can be assigned to a job posting.

    Attributes:
        FULL_TIME (str): Full-time schedule.
        SHIFT (str): Shift-based schedule.
        FLEXIBLE (str): Flexible schedule.
        REMOTE (str): Remote work.
    """

    FULL_TIME = "full", _("Full-time")
    SHIFT = "shift", _("Shift schedule")
    FLEXIBLE = "flex", _("Flexible schedule")
    REMOTE = "remote", _("Remote work")
