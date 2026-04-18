from decimal import Decimal
from typing import Any

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.catalog.models import Product
from apps.core.models import BaseModel


class OrderItem(BaseModel):  # type: ignore
    order = models.ForeignKey(
        to="Order",
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name=_("order"),
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name=_("product"),
    )
    quantity = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal(value="1.00"),
        verbose_name=_("quantity"),
    )
    product_name_snapshot = models.CharField(
        max_length=255,
        verbose_name=_("product name snapshot"),
    )
    price_snapshot = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        verbose_name=_("price snapshot"),
    )
    total_price = models.GeneratedField(
        expression=models.ExpressionWrapper(
            expression=models.F("price_snapshot") * models.F("quantity"),
            output_field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
        output_field=models.DecimalField(max_digits=10, decimal_places=2),
        db_persist=True,
        editable=False,
        verbose_name=_("total price"),
        help_text=_("Calculated by the system."),
    )

    class Meta:
        db_table = "orders_order_item"
        db_table_comment = "Table containing order items."
        verbose_name = _("order item")
        verbose_name_plural = _("order items")
        constraints = [
            models.UniqueConstraint(
                fields=["order", "product"],
                name="unique_order_product",
                violation_error_message=_("This product is already in order."),
            ),
        ]
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.order}: {self.product} x {self.quantity}"

    def save(self, **kwargs: Any) -> None:
        if not self.price_snapshot:
            self.price_snapshot = self.product.final_price
        if not self.product_name_snapshot:
            self.product_name_snapshot = self.product.name
        super().save(**kwargs)
