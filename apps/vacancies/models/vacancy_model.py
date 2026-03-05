from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy
from django_stubs_ext import StrOrPromise

from apps.core.models import BaseModel
from apps.vacancies.choices import WorkExperience, WorkSchedule


class Vacancy(BaseModel):  # type: ignore
    title = models.CharField(
        max_length=255,
        verbose_name=_("title"),
    )
    short_description = models.TextField(
        verbose_name=_("short description"),
    )
    description = models.TextField(
        verbose_name=_("description"),
        help_text=_("Text or HTML markup: div, ul, h3, li."),
    )
    professional_area = models.ForeignKey(
        to="ProfessionalArea",
        on_delete=models.PROTECT,
        related_name="vacancies",
        verbose_name=_("professional area"),
    )
    city = models.ForeignKey(
        to="City",
        on_delete=models.PROTECT,
        related_name="vacancies",
        verbose_name=_("city"),
    )
    work_schedule = models.CharField(
        max_length=10,
        choices=WorkSchedule.choices,
        default=WorkSchedule.FULL_TIME,
        verbose_name=_("work schedule"),
    )
    work_experience = models.CharField(
        max_length=10,
        choices=WorkExperience.choices,
        default=WorkExperience.NO_EXPERIENCE,
        verbose_name=_("work experience"),
    )
    salary_from = models.PositiveIntegerField(
        verbose_name=_("salary from"),
        null=True,
        blank=True,
    )
    salary_to = models.PositiveIntegerField(
        verbose_name=_("salary to"),
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=pgettext_lazy("feminine", "active"),
    )

    class Meta:
        db_table = "vacancies_vacancy"
        db_table_comment = "Table containing vacancies."
        verbose_name = _("vacancy")
        verbose_name_plural = _("vacancies")
        ordering = (
            "-created_at",
            "title",
        )
        constraints = [
            models.CheckConstraint(
                name="check_vacancy_salary_from_lt_salary_to",
                check=(
                    models.Q(salary_from__isnull=True)
                    | models.Q(salary_to__isnull=True)
                    | models.Q(salary_from__lt=models.F("salary_to"))
                ),
                violation_error_message=_(
                    "Maximum salary must be greater than minimum salary."
                ),
            )
        ]

    def __str__(self) -> str:
        return f"{self.title} / {self.city}"

    @property
    def formatted_salary(self) -> StrOrPromise:
        if self.salary_from and self.salary_to:
            return _("%(salary_from)s – %(salary_to)s") % {
                "salary_from": self.salary_from,
                "salary_to": self.salary_to,
            }
        elif self.salary_from:
            return _("from %(salary_from)s") % {
                "salary_from": self.salary_from
            }
        elif self.salary_to:
            return _("to %(salary_to)s") % {"salary_to": self.salary_to}
        return ""

    def get_absolute_url(self) -> str:
        return reverse(
            viewname="vacancies:detail", kwargs={"vacancy_pk": self.pk}
        )
