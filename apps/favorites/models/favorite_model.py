from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.catalog.models import Product
from apps.core.models import BaseModel


class Favorite(BaseModel):  # type: ignore
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name=_("user"),
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="favorites",
        verbose_name=_("product"),
    )

    class Meta:
        db_table = "favorites_favorite"
        db_table_comment = "Table containing favorites."
        verbose_name = _("favorite")
        verbose_name_plural = _("favorites")
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_user_product",
                violation_error_message=_(
                    "This product is already in favorites."
                ),
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user}: {self.product}"
