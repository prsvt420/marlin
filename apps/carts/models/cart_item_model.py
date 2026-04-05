from decimal import Decimal
from typing import Any

from django.db import models
from django.db.models import ExpressionWrapper, F
from django.utils.translation import gettext_lazy as _

from apps.catalog.models import Product
from apps.core.models import BaseModel


class CartItem(BaseModel):  # type: ignore
    cart = models.ForeignKey(
        to="Cart",
        on_delete=models.CASCADE,
        related_name="cart_items",
        verbose_name=_("cart"),
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
        verbose_name=_("product"),
    )
    quantity = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal(value="1.00"),
        verbose_name=_("quantity"),
    )
    price_snapshot = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        verbose_name=_("price snapshot"),
    )
    total_price = models.GeneratedField(
        expression=ExpressionWrapper(
            expression=F("price_snapshot") * F("quantity"),
            output_field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
        output_field=models.DecimalField(max_digits=10, decimal_places=2),
        db_persist=True,
        editable=False,
        verbose_name=_("total price"),
        help_text=_("Calculated by the system."),
    )

    class Meta:
        db_table = "carts_cart_item"
        db_table_comment = "Table containing cart items."
        verbose_name = _("cart item")
        verbose_name_plural = _("cart items")
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_cart_product",
                violation_error_message=_(
                    "This product is already in your cart."
                ),
            ),
        ]
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.cart}: {self.product} x {self.quantity}"

    def save(self, **kwargs: Any) -> None:
        if not self.price_snapshot:
            self.price_snapshot = self.product.final_price
        super().save(**kwargs)
