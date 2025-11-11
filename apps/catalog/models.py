from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.catalog.choices import UnitType


class Product(models.Model):
    """Model representing a product in the catalog.

    Each record stores information about a single product:
    name, description, composition, category, SKU, price, discount,
    stock availability, unit type, and status of activity.

    Attributes:
        name (CharField): Product name.
        description (TextField): Product description.
        slug (SlugField): Unique slug for the product.
        composition (TextField): Composition of the product.
        unit_type (CharField): Measurement unit (e.g., pcs, kg, l).
        price (DecimalField): Product price.
        discount (DecimalField): Discount percentage.
        category (ForeignKey): Category the product belongs to.
        sku (CharField): Stock Keeping Unit (SKU).
        stock (PositiveIntegerField): Quantity in stock.
        is_active (BooleanField): Whether the product is visible
            in the catalog.
        created_at (DateTimeField): Date and time when the product
            was created.
        updated_at (DateTimeField): Date and time when the product
            was last updated.
    """

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

    def __str__(self) -> str:
        """Return a string representation of the product.

        Returns:
            str: Product name with SKU.
        """
        return f"{self.name} ({self.sku})"

    def get_final_price(self) -> Decimal:
        """Return price with discount applied.

        Returns:
            Decimal: Final price.
        """
        return self.price * (1 - self.discount / Decimal("100"))

    def get_absolute_url(self) -> str:
        """Return the absolute URL for the product detail page.

        Uses the product's slug to reverse the URL named
        'catalog:product_detail'.

        Returns:
            str: The URL of the product detail page.
        """
        return reverse("catalog:product_detail", kwargs={"slug": self.slug})


class ProductNutrition(models.Model):
    """Model representing nutritional values of a product.

    Each record stores the nutritional information for a single product:
    calories, proteins, fats, and carbohydrates.
    The relationship is defined as one-to-one with the Product model.

    Attributes:
        product (OneToOneField): The product this nutrition info belongs to.
        calories (DecimalField): Calories (kcal).
        proteins (DecimalField): Proteins (g).
        fats (DecimalField): Fats (g).
        carbs (DecimalField): Carbs (g).
    """

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

    def __str__(self) -> str:
        """Return a string representation of the nutrition object.

        Returns:
            str: Product name with it's nutritional values.
        """
        return (
            f"{self.product.name} "
            f"({_('Calories')}: {self.calories or '—'} {_('kcal')}, "
            f"{_('Proteins')}: {self.proteins or '—'} {_('g')}, "
            f"{_('Fats')}: {self.fats or '—'} {_('g')}, "
            f"{_('Carbs')}: {self.carbs or '—'} {_('g')})"
        )


class Attribute(models.Model):
    """Model representing a product attribute.

    Stores available attributes that can be assigned to products,
    such as weight, shelf life, or storage conditions.

    Attributes:
        name (CharField): The name of the attribute.
    """

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

    def __str__(self) -> str:
        """Return a string representation of the attribute.

        Returns:
            str: Attribute name.
        """
        return f"{self.name}"


class ProductAttribute(models.Model):
    """Model representing a product's specific attribute value.

    Defines the relationship between products and their attributes.
    Each record assigns a specific value of an attribute to a product.

    Attributes:
        product (ForeignKey): The product this attribute belongs to.
        attribute (ForeignKey): The attribute assigned to the product.
        value (CharField): The specific value of the attribute.
    """

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

    def __str__(self) -> str:
        """Return a string representation of product attribute.

        Returns:
            str: Product name, attribute, and its value.
        """
        return f"{self.product.name} - {self.attribute.name}: {self.value}"


class Category(models.Model):
    """Model representing product categories.

    Categories allow grouping of products into hierarchical structures.
    Each category may have a parent category (for nesting).

    Attributes:
        parent (ForeignKey): The parent category (nullable).
        name (CharField): The name of the category.
        slug (SlugField): Unique slug for the category.
        description (TextField): Description of the category.
        sort_order (PositiveIntegerField): Order of appearance in lists.
        is_active (BooleanField): Whether the category is active.
        created_at (DateTimeField): When the category was created.
        updated_at (DateTimeField): Last update timestamp.
    """

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

    def __str__(self) -> str:
        """Return the category name.

        Returns:
            str: The name of the category.
        """
        return f"{self.name}"


class ProductImage(models.Model):
    """Model representing images of a product.

    Each record stores a reference to an image of a product,
    along with its alt text and display order.

    Attributes:
        product (ForeignKey): The product this image belongs to.
        image_path (ImageField): Path to the image file.
        alt_text (CharField): Alternative text for the image.
        sort_order (PositiveIntegerField): The order of image display.
    """

    product = models.ForeignKey(
        to="Product",
        on_delete=models.CASCADE,
        related_name="product_images",
        verbose_name="продукт",
        help_text="Продукт, к которому относится изображение.",
    )
    image_path = models.ImageField(
        upload_to="product_images/",
        verbose_name="изображение",
        help_text="Путь к изображению продукта.",
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="альтернативный текст",
        help_text="Описание изображения для SEO и доступности.",
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="порядок отображения",
        help_text="Порядок сортировки изображений продукта.",
    )

    class Meta:  # noqa: D106
        db_table = "catalog_product_image"
        db_table_comment = "Таблица с изображениями продуктов"
        verbose_name = "изображение продукта"
        verbose_name_plural = "изображения продукта"
        ordering = ("product__name", "sort_order")

    def __str__(self) -> str:
        """Return a string representation of the product image.

        Returns:
            str: Product name with image path.
        """
        return f"{self.product.name} - {self.image_path}"
