from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductNutrition(models.Model):  # type: ignore
    product = models.OneToOneField(
        to="Product",
        on_delete=models.CASCADE,
        related_name="product_nutrition",
        verbose_name=_("product"),
        help_text=_("The product to which the nutritional value belongs."),
    )
    calories = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("calories"),
        help_text=_("Calories (kcal)."),
    )
    proteins = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("proteins"),
        help_text=_("Proteins (g)."),
    )
    fats = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("fats"),
        help_text=_("Fats (g)."),
    )
    carbs = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("carbs"),
        help_text=_("Carbs (g)."),
    )

    class Meta:
        db_table = "catalog_product_nutrition"
        db_table_comment = "Table containing nutritional values of products."
        verbose_name = _("nutritional value")
        verbose_name_plural = _("nutritional values")
        ordering = ("product__name",)

    def __str__(self) -> str:
        return (
            f"{self.product.name} "
            f"({_('Calories')}: {self.calories or '—'} {_('kcal')}, "
            f"{_('Proteins')}: {self.proteins or '—'} {_('g')}, "
            f"{_('Fats')}: {self.fats or '—'} {_('g')}, "
            f"{_('Carbs')}: {self.carbs or '—'} {_('g')})"
        )
