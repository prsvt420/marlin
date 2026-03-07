from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from apps.core.models import BaseModel


class ProductImage(BaseModel):  # type: ignore
    product = models.ForeignKey(
        to="Product",
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("product"),
    )
    image = ResizedImageField(
        size=(1024, 1024),
        crop=None,
        quality=80,
        force_format="WEBP",
        upload_to="product_images/",
        keep_meta=False,
        verbose_name=_("image"),
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("sort order"),
    )

    class Meta:
        db_table = "catalog_product_image"
        db_table_comment = "Table containing product images."
        verbose_name = _("product image")
        verbose_name_plural = _("product images")
        ordering = ("product__name", "sort_order")

    def __str__(self) -> str:
        return f"{self.product.name} - {self.image}"
