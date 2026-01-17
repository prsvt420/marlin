from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise

from apps.vacancies.choices import ExperienceLevel, WorkSchedule


class Vacancy(models.Model):
    """Model for vacancy."""

    title = models.CharField(
        max_length=255,
        verbose_name=_("title"),
        help_text=_("Vacancy title."),
    )
    short_description = models.TextField(
        verbose_name=_("short description"),
        help_text=_("Brief introductory text about the vacancy."),
    )
    description = models.TextField(
        verbose_name=_("description"),
        help_text=_(
            "Detailed description of the vacancy "
            "(HTML markup, use div, ul, h3, li)."
        ),
    )
    professional_area = models.ForeignKey(
        to="ProfessionalArea",
        on_delete=models.CASCADE,
        related_name="vacancies",
        verbose_name=_("professional area"),
        help_text=_("Professional field of the vacancy."),
    )
    city = models.ForeignKey(
        to="City",
        on_delete=models.CASCADE,
        related_name="vacancies",
        verbose_name=_("city and region"),
        help_text=_("City and region where the vacancy is posted."),
    )
    work_schedule = models.CharField(
        max_length=10,
        choices=WorkSchedule.choices,
        default=WorkSchedule.FULL_TIME,
        verbose_name=_("work schedule"),
        help_text=_("Expected work schedule."),
    )
    experience_level = models.CharField(
        max_length=10,
        choices=ExperienceLevel.choices,
        default=ExperienceLevel.NO_EXPERIENCE,
        verbose_name=_("experience level"),
        help_text=_("Required work experience level."),
    )
    salary_from = models.PositiveIntegerField(
        verbose_name=_("salary from"),
        help_text=_("Minimum salary."),
        null=True,
        blank=True,
    )
    salary_to = models.PositiveIntegerField(
        verbose_name=_("salary to"),
        help_text=_("Maximum salary."),
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("active"),
        help_text=_("Determines whether the vacancy is visible."),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created date"),
        help_text=_("Date and time when the vacancy was added."),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated date"),
        help_text=_("Date and time when the vacancy was last updated."),
    )

    class Meta:  # noqa: D106
        db_table = "vacancies_vacancy"
        db_table_comment = "Table containing job vacancies."
        verbose_name = _("vacancy")
        verbose_name_plural = _("vacancies")
        ordering = (
            "-created_at",
            "title",
        )

    def __str__(self) -> str:  # noqa: D105
        return f"{self.title} / {self.city}"

    def get_formatted_salary(self) -> StrOrPromise:
        """Return the salary range formatted."""
        if self.salary_from and self.salary_to:
            return _("%(from)s – %(to)s") % {
                "from": self.salary_from,
                "to": self.salary_to,
            }
        elif self.salary_from:
            return _("from %(from)s") % {"from": self.salary_from}
        elif self.salary_to:
            return _("to %(to)s") % {"to": self.salary_to}
        return ""

    def clean(self) -> None:
        """Validate vacancy data."""
        super().clean()
        if (
            self.salary_from
            and self.salary_to  # noqa: W503
            and self.salary_from >= self.salary_to  # noqa: W503
        ):
            raise ValidationError(
                {
                    "salary_to": _(
                        "Maximum salary must be greater "
                        "than minimum salary."
                    )
                }
            )

    def get_absolute_url(self) -> str:
        """Return the URL to access the detail view of this vacancy."""
        return reverse("vacancies:vacancy_detail", kwargs={"pk": self.pk})
