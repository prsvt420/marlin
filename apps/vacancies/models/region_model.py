from django.db import models
from django.utils.translation import gettext_lazy as _


class Region(models.Model):  # type: ignore
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("name"),
        help_text=_("Region name."),
    )

    class Meta:
        db_table = "vacancies_region"
        db_table_comment = "Table containing regions."
        verbose_name = _("region")
        verbose_name_plural = _("regions")
        ordering = ("name",)

    def __str__(self) -> str:
        return f"{self.name}"
