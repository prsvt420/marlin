from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductAttribute(models.Model):  # type: ignore
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

    class Meta:
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
        return f"{self.product.name} - {self.attribute.name}: {self.value}"
