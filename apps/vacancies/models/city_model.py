from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext import StrOrPromise

from apps.core.models import BaseModel


class City(BaseModel):  # type: ignore
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("name"),
    )
    region = models.ForeignKey(
        to="Region",
        on_delete=models.PROTECT,
        related_name="cities",
        verbose_name=_("region"),
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "vacancies_city"
        db_table_comment = "Table containing cities."
        verbose_name = _("city")
        verbose_name_plural = _("cities")
        ordering = ("name",)

    def __str__(self) -> str:
        prefix: StrOrPromise = _("city of")

        if self.region:
            return f"{prefix} {self.name}, {self.region.name}"
        return f"{prefix} {self.name}"
