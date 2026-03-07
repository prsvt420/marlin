from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class ProductNutrition(BaseModel):  # type: ignore
    product = models.OneToOneField(
        to="Product",
        on_delete=models.CASCADE,
        related_name="nutrition",
        verbose_name=_("product"),
    )
    calories = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        verbose_name=_("calories"),
    )
    proteins = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        verbose_name=_("proteins"),
    )
    fats = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        verbose_name=_("fats"),
    )
    carbs = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        verbose_name=_("carbs"),
    )

    class Meta:
        db_table = "catalog_product_nutrition"
        db_table_comment = "Table containing product nutritions"
        verbose_name = _("product nutrition")
        verbose_name_plural = _("product nutritions")
        ordering = ("product__name",)

    def __str__(self) -> str:
        return f"{self.product.name}"
