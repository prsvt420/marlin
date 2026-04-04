from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

from apps.catalog.choices import UnitType
from apps.core.models import BaseModel


class Product(BaseModel):  # type: ignore
    name = models.CharField(
        max_length=255,
        verbose_name=_("name"),
    )
    description = models.TextField(
        verbose_name=_("description"),
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name=_("slug"),
    )
    composition = models.TextField(
        max_length=255,
        blank=True,
        verbose_name=_("composition"),
    )
    attributes = models.JSONField(
        default=dict, blank=True, verbose_name=_("attributes")
    )
    unit_type = models.CharField(
        max_length=10,
        choices=UnitType.choices,
        default=UnitType.PIECE,
        verbose_name=_("unit type"),
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("price"),
    )
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name=_("discount"),
    )
    final_price = models.GeneratedField(
        expression=models.ExpressionWrapper(
            expression=models.F("price")
            * (models.Value(1) - models.F("discount") / models.Value(100.0)),
            output_field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
        output_field=models.DecimalField(max_digits=10, decimal_places=2),
        db_persist=True,
        editable=False,
        verbose_name=_("final price"),
        help_text=_("Calculated by the system."),
    )
    is_available = models.GeneratedField(
        expression=models.Case(
            models.When(is_active=True, stock__gt=0, then=True),
            default=False,
            output_field=models.BooleanField(),
        ),
        output_field=models.BooleanField(),
        db_persist=True,
        editable=False,
        verbose_name=_("availability"),
        help_text=_("Calculated by the system."),
    )
    category = models.ForeignKey(
        to="Category",
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("category"),
    )
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name=_("stock"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=pgettext_lazy("masculine", "active"),
    )

    class Meta:
        db_table = "catalog_product"
        db_table_comment = "Table containing products."
        verbose_name = _("product")
        verbose_name_plural = _("products")
        ordering = ("-created_at", "name")
        indexes = [
            GinIndex(
                fields=["attributes"], name="index_product_attributes_gin"
            )
        ]

    def __str__(self) -> str:
        return f"{self.name}"

    def get_absolute_url(self) -> str:
        return reverse(
            viewname="catalog:product-detail",
            kwargs={
                "category_slug": self.category.slug,
                "product_slug": self.slug,
            },
        )
