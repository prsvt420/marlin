from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise


class City(models.Model):
    """Model for city."""

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("name"),
        help_text=_("City name."),
    )
    region = models.ForeignKey(
        to="Region",
        on_delete=models.CASCADE,
        related_name="cities",
        verbose_name=_("region"),
        help_text=_("Region to which the city belongs."),
        null=True,
        blank=True,
    )

    class Meta:  # noqa: D106
        db_table = "vacancies_city"
        db_table_comment = "Table containing cities."
        verbose_name = _("city")
        verbose_name_plural = _("cities")
        ordering = ("name",)

    def __str__(self) -> str:  # noqa: D105
        prefix: StrOrPromise = _("city of")

        if self.region:
            return f"{prefix} {self.name}, {self.region.name}"
        return f"{prefix} {self.name}"
