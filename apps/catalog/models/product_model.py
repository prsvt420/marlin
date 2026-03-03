from django.db import models
from django.db.models import ExpressionWrapper, F
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.catalog.choices import UnitType


class Product(models.Model):  # type: ignore
    name = models.CharField(
        max_length=255,
        verbose_name=_("name"),
        help_text=_("Product name."),
    )
    description = models.TextField(
        verbose_name=_("description"),
        help_text=_("Product description."),
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name=_("URL-identifier"),
        help_text=_("Unique URL identifier (letters, numbers, hyphens)."),
    )
    composition = models.TextField(
        verbose_name=_("composition"),
        help_text=_("Product composition."),
    )
    unit_type = models.CharField(
        max_length=10,
        choices=UnitType.choices,
        default=UnitType.PIECE,
        verbose_name=_("unit type"),
        help_text=_("Unit of measurement of the product (e.g., kg, l, pcs)."),
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("price"),
        help_text=_("Product price."),
    )
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name=_("discount"),
        help_text=_("Product discount in percent."),
    )
    final_price = models.GeneratedField(
        expression=ExpressionWrapper(
            expression=F("price") * (1 - F("discount") / 100.0),
            output_field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
        output_field=models.DecimalField(max_digits=10, decimal_places=2),
        db_persist=True,
        verbose_name=_("final price"),
        help_text=_("Product final price (autocalculated)."),
    )
    is_available = models.GeneratedField(
        expression=models.Case(
            models.When(is_active=True, stock__gt=0, then=True),
            default=False,
            output_field=models.BooleanField(),
        ),
        output_field=models.BooleanField(),
        db_persist=True,
        verbose_name=_("availability"),
        help_text=_("Product availability (autocalculated)."),
    )
    category = models.ForeignKey(
        to="Category",
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("category"),
        help_text=_("The category to which the product belongs."),
    )
    sku = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="SKU",
        help_text=_("Stock Keeping Unit (SKU)."),
    )
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name=_("stock"),
        help_text=_("Number of products in stock."),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("active"),
        help_text=_(
            "Determines whether the product is displayed in the catalog."
        ),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created date"),
        help_text=_("Date and time the product was added."),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated date"),
        help_text=_("Date and time when the product was last updated."),
    )

    class Meta:
        db_table = "catalog_product"
        db_table_comment = "Table containing product information."
        verbose_name = _("product")
        verbose_name_plural = _("products")
        ordering = (
            "-created_at",
            "name",
        )

    def __str__(self) -> str:
        return f"{self.name} ({self.sku})"

    def get_absolute_url(self) -> str:
        return reverse(
            viewname="catalog:product-detail",
            kwargs={
                "category_slug": self.category.slug,
                "product_slug": self.slug,
            },
        )
