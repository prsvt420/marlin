from decimal import ROUND_HALF_UP, Decimal
from typing import List, Optional

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.catalog.choices import UnitType


class Product(models.Model):
    """Model for product."""

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

    class Meta:  # noqa: D106
        db_table = "catalog_product"
        db_table_comment = "Table containing product information."
        verbose_name = _("product")
        verbose_name_plural = _("products")
        ordering = (
            "-created_at",
            "name",
        )

    def __str__(self) -> str:  # noqa: D105
        return f"{self.name} ({self.sku})"

    def get_final_price(self) -> Decimal:
        """Return the price with discount applied."""
        final_price: Decimal = self.price * (
            1 - self.discount / Decimal("100")
        )
        return final_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def get_absolute_url(self) -> str:
        """Return the URL to access the detail view of this product."""
        return reverse("catalog:product_detail", kwargs={"slug": self.slug})


class ProductNutrition(models.Model):
    """Model for product nutrition."""

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

    class Meta:  # noqa: D106
        db_table = "catalog_product_nutrition"
        db_table_comment = "Table containing nutritional values of products."
        verbose_name = _("nutritional value")
        verbose_name_plural = _("nutritional values")
        ordering = ("product__name",)

    def __str__(self) -> str:  # noqa: D105
        return (
            f"{self.product.name} "
            f"({_('Calories')}: {self.calories or '—'} {_('kcal')}, "
            f"{_('Proteins')}: {self.proteins or '—'} {_('g')}, "
            f"{_('Fats')}: {self.fats or '—'} {_('g')}, "
            f"{_('Carbs')}: {self.carbs or '—'} {_('g')})"
        )


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


class ProductAttribute(models.Model):
    """Model for product attribute."""

    product = models.ForeignKey(
        to="Product",
        on_delete=models.CASCADE,
        related_name="product_attributes",
        verbose_name=_("product"),
        help_text=_("The product to which the attribute belongs."),
    )
    attribute = models.ForeignKey(
        to="Attribute",
        on_delete=models.CASCADE,
        related_name="attribute_values",
        verbose_name=_("attribute"),
        help_text=_(
            "The product attribute (e.g., weight, "
            "shelf life, storage conditions)."
        ),
    )
    value = models.CharField(
        max_length=255,
        verbose_name=_("value"),
        help_text=_(
            "The specific value of the attribute (e.g., 500 g, 12 months)."
        ),
    )

    class Meta:  # noqa: D106
        db_table = "catalog_product_attribute"
        db_table_comment = "Table containing product attribute values."
        verbose_name = _("product attribute")
        verbose_name_plural = _("product attributes")
        constraints = [
            models.UniqueConstraint(
                fields=["product", "attribute"],
                name="unique_product_attribute",
            )
        ]

    def __str__(self) -> str:  # noqa: D105
        return f"{self.product.name} - {self.attribute.name}: {self.value}"


class Category(models.Model):
    """Model for category."""

    parent = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        related_name="subcategories",
        null=True,
        blank=True,
        verbose_name=_("parent category"),
        help_text=_("Parent category (if nesting is used)."),
    )
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("name"),
        help_text=_("Category name."),
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name=_("URL-identifier"),
        help_text=_("Unique URL identifier (letters, numbers, hyphens)."),
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("description"),
        help_text=_("Category description."),
    )
    image_path = models.ImageField(
        upload_to="category_images/",
        blank=True,
        null=True,
        verbose_name=_("image"),
        help_text=_("Path to the category image."),
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("alternative text"),
        help_text=_("Description of the image for SEO and accessibility."),
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("display order"),
        help_text=_("Order in which categories appear in lists."),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("active"),
        help_text=_(
            "Determines whether the category is displayed in the catalog."
        ),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created date"),
        help_text=_("Date and time the category was added."),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated date"),
        help_text=_("Date and time when the category was last updated."),
    )

    class Meta:  # noqa: D106
        db_table = "catalog_category"
        db_table_comment = "Table containing product categories."
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ("sort_order", "name")

    def __str__(self) -> str:  # noqa: D105
        return f"{self.name}"

    def get_hierarchy(self) -> List["Category"]:
        """Return the category hierarchy."""
        hierarchy: List[Category] = []
        category: Optional[Category] = self

        while category is not None:
            hierarchy.append(category)
            category = category.parent

        hierarchy.reverse()

        return hierarchy

    def get_absolute_url(self) -> str:
        """Return the URL to access the product list view of this category."""
        return reverse("catalog:product_list", kwargs={"slug": self.slug})


class ProductImage(models.Model):
    """Model for product image."""

    product = models.ForeignKey(
        to="Product",
        on_delete=models.CASCADE,
        related_name="product_images",
        verbose_name=_("product"),
        help_text=_("The product to which the image belongs."),
    )
    image_path = models.ImageField(
        upload_to="product_images/",
        verbose_name=_("image"),
        help_text=_("Path to the product image."),
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("alternative text"),
        help_text=_("Description of the image for SEO and accessibility."),
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("display order"),
        help_text=_("Order in which product images appear in lists."),
    )

    class Meta:  # noqa: D106
        db_table = "catalog_product_image"
        db_table_comment = "Table containing product images."
        verbose_name = _("product image")
        verbose_name_plural = _("product images")
        ordering = ("product__name", "sort_order")

    def __str__(self) -> str:  # noqa: D105
        return f"{self.product.name} - {self.image_path}"
