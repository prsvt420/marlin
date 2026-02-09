from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(models.Model):  # type: ignore

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

    class Meta:
        db_table = "catalog_category"
        db_table_comment = "Table containing product categories."
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ("sort_order", "name")

    def __str__(self) -> str:
        return f"{self.name}"

    def get_absolute_url(self) -> str:
        return reverse(
            viewname="catalog:product-list",
            kwargs={"category_slug": self.slug},
        )
