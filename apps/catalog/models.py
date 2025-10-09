from decimal import Decimal

from django.db import models

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
        verbose_name="Название",
        help_text="Название продукта",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Описание продукта",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="URL-идентификатор",
        help_text="Уникальное имя для URL (латиница, дефисы)",
    )
    composition = models.TextField(
        verbose_name="Состав",
        help_text="Состав продукта",
    )
    unit_type = models.CharField(
        max_length=10,
        choices=UnitType.choices,
        default=UnitType.PIECE,
        verbose_name="Единица измерения",
        help_text="Единица измерения продукта (например: кг, л, шт)",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        help_text="Цена продукта",
    )
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Скидка (%)",
        help_text="Скидка на продукт в процентах",
    )
    category = models.ForeignKey(
        to="Category",
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
        help_text="Категория, к которой относится продукт",
    )
    sku = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="SKU",
        help_text="Артикул (Stock Keeping Unit)",
    )
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Остаток",
        help_text="Количество продуктов на складе",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        help_text="Определяет, показывается ли продукт в каталоге",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время добавления продукта",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
        help_text="Дата и время последнего обновления",
    )

    class Meta:  # noqa: D106
        db_table = "products"
        db_table_comment = "Таблица с информацией о продуктах"
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ("name",)

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
        carbs (DecimalField): Carbohydrates (g).
    """

    product = models.OneToOneField(
        to="Product",
        on_delete=models.CASCADE,
        related_name="product_nutrition",
        verbose_name="Продукт",
        help_text="Продукт, к которому относится данная пищевая ценность",
    )
    calories = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Калории",
        help_text="Калории (ккал)",
    )
    proteins = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Белки",
        help_text="Белки (г)",
    )
    fats = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Жиры",
        help_text="Жиры (г)",
    )
    carbs = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Углеводы",
        help_text="Углеводы (г)",
    )

    class Meta:  # noqa: D106
        db_table = "product_nutritions"
        db_table_comment = "Таблица с информацией о пищевой ценности продуктов"
        verbose_name = "пищевая ценность"
        verbose_name_plural = "пищевая ценность"
        ordering = ("product__name",)

    def __str__(self) -> str:
        """Return a string representation of the nutrition object.

        Returns:
            str: Product name with it's nutritional values.
        """
        return (
            f"{self.product.name} "
            f"(Calories: {self.calories or '-'} kcal, "
            f"Proteins: {self.proteins or '-'} g, "
            f"Fats: {self.fats or '-'} g, "
            f"Carbs: {self.carbs or '-'} g)"
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
        verbose_name="Название",
        help_text=(
            "Название атрибута (например: "
            "вес, срок хранения, условия хранения)"
        ),
    )

    class Meta:  # noqa: D106
        db_table = "attributes"
        db_table_comment = "Таблица с возможными атрибутами продуктов"
        verbose_name = "атрибут"
        verbose_name_plural = "атрибуты"
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
        verbose_name="Продукт",
        help_text="Продукт, к которому относится атрибут",
    )
    attribute = models.ForeignKey(
        to="Attribute",
        on_delete=models.CASCADE,
        related_name="attribute_values",
        verbose_name="Атрибут",
        help_text=(
            "Атрибут продукта (например: вес, срок хранения, условия хранения)"
        ),
    )
    value = models.CharField(
        max_length=255,
        verbose_name="Значение",
        help_text="Значение атрибута (например: 500 г, 12 месяцев)",
    )

    class Meta:  # noqa: D106
        db_table = "product_attributes"
        db_table_comment = "Таблица со значениями атрибутов продуктов"
        verbose_name = "атрибут продукта"
        verbose_name_plural = "атрибуты продуктов"
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
        verbose_name="Родительская категория",
        help_text="Родительская категория (если есть вложенность)",
    )
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Название",
        help_text="Название категории",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="URL-идентификатор",
        help_text="Уникальное имя для URL (латиница, дефисы)",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
        help_text="Описание категории",
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок отображения",
        help_text="Порядок сортировки категорий в списке",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
        help_text="Определяет, показывается ли категория в каталоге",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время добавления категории",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
        help_text="Дата и время последнего обновления категории",
    )

    class Meta:  # noqa: D106
        db_table = "categories"
        db_table_comment = "Таблица с категориями продуктов"
        verbose_name = "категория"
        verbose_name_plural = "категории"
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
        related_name="images",
        verbose_name="Продукт",
        help_text="Продукт, к которому относится изображение",
    )
    image_path = models.ImageField(
        upload_to="product_images/",
        verbose_name="Изображение",
        help_text="Путь к изображению продукта",
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Альтернативный текст",
        help_text="Описание изображения для SEO и доступности",
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок отображения",
        help_text="Порядок сортировки изображений продукта",
    )

    class Meta:  # noqa: D106
        db_table = "product_images"
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
