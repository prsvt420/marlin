from django.db import models
from django.utils.translation import gettext_lazy as _


class ProfessionalArea(models.Model):
    """Model for professional area."""

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("name"),
        help_text=_("Professional area name."),
    )

    class Meta:  # noqa: D106
        db_table = "vacancies_professional_area"
        db_table_comment = "Table containing professional areas."
        verbose_name = _("professional area")
        verbose_name_plural = _("professional areas")
        ordering = ("name",)

    def __str__(self) -> str:  # noqa: D105
        return f"{self.name}"
