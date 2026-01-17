from typing import Any

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.catalog.models import Product


class CartItem(models.Model):
    """Model for cart item."""

    cart = models.ForeignKey(
        to="Cart",
        on_delete=models.CASCADE,
        related_name="cart_items",
        verbose_name=_("cart"),
        help_text=_("The cart to which the cart item belongs."),
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
        verbose_name=_("product"),
        help_text=_("Product belonging to the cart item."),
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_("quantity"),
        help_text=_("Number of products in cart item."),
    )
    price_snapshot = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("price snapshot"),
        help_text=_(
            "Price of the product at the time it was added to the cart."
        ),
    )

    class Meta:  # noqa: D106
        db_table = "carts_cart_item"
        db_table_comment = "Table containing cart items."
        verbose_name = _("cart item")
        verbose_name_plural = _("cart items")
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_cart_product",
            ),
            models.CheckConstraint(
                check=models.Q(quantity__gt=0),
                name="constraint_quantity_gt_zero",
            ),
        ]

    def __str__(self) -> str:  # noqa: D105
        return f"{self.cart}: {self.product} x {self.quantity}"

    def save(self, **kwargs: Any) -> None:
        """Save cart item data."""
        if not self.price_snapshot:
            self.price_snapshot = self.product.get_final_price()
        super().save(**kwargs)
