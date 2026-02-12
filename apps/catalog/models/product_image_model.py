from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductImage(models.Model):  # type: ignore
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

    class Meta:
        db_table = "catalog_product_image"
        db_table_comment = "Table containing product images."
        verbose_name = _("product image")
        verbose_name_plural = _("product images")
        ordering = ("product__name", "sort_order")

    def __str__(self) -> str:
        return f"{self.product.name} - {self.image_path}"
