from django.db import models
from django.utils.translation import gettext_lazy as _


class Attribute(models.Model):
    """Model for attribute."""

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("name"),
        help_text=_(
            "Name of the attribute (e.g., weight, "
            "shelf life, storage conditions)."
        ),
    )

    class Meta:  # noqa: D106
        db_table = "catalog_attribute"
        db_table_comment = "Table containing possible product attributes."
        verbose_name = _("attribute")
        verbose_name_plural = _("attributes")
        ordering = ("name",)

    def __str__(self) -> str:  # noqa: D105
        return f"{self.name}"
