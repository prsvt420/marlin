from django.db import models


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

    NO_EXPERIENCE = "no_exp", "Без опыта"
    ONE_TO_THREE = "1_3", "От 1 года до 3 лет"
    THREE_TO_SIX = "3_6", "От 3 до 6 лет"
    MORE_THAN_SIX = "6_plus", "Более 6 лет"


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

    FULL_TIME = "full", "Полный день"
    SHIFT = "shift", "Сменный график"
    FLEXIBLE = "flex", "Гибкий график"
    REMOTE = "remote", "Удаленная работа"
