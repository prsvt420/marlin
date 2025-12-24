from decimal import ROUND_HALF_UP, Decimal
from typing import Any

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.carts.choices import CartStatus
from apps.catalog.models import Product


class Cart(models.Model):
    """Model representing a cart.

    Attributes:
        user (ForeignKey): The user to whom the cart belongs.
        cart_status (CharField): Cart status (active, ordered, abandoned).
        created_at (DateTimeField): Date and time the cart was created.
        updated_at (DateTimeField): Date and time when the cart was last
            updated.
    """

    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="carts",
        verbose_name=_("user"),
        help_text=_("The user to which the cart belongs."),
    )
    cart_status = models.CharField(
        max_length=20,
        choices=CartStatus.choices,
        default=CartStatus.ACTIVE,
        verbose_name=_("cart status"),
        help_text=_("Current cart status (active, converted, abandoned)."),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("created date"),
        help_text=_("Date and time the cart was created."),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("updated date"),
        help_text=_("Date and time when the cart was last updated."),
    )

    class Meta:  # noqa: D106
        db_table = "carts_cart"
        db_table_comment = "Table containing carts."
        verbose_name = _("cart")
        verbose_name_plural = _("carts")
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=models.Q(cart_status=CartStatus.ACTIVE),
                name="unique_active_cart_user",
                violation_error_message=_(
                    "A user can have only one active cart."
                ),
            ),
        ]

    def get_total_price(self) -> Decimal:
        """Return the cart total price.

        Returns:
            Decimal: Cart total price.
        """
        total_price: Decimal = self.cart_items.aggregate(
            total_price=models.Sum(
                models.F("price_snapshot") * models.F("quantity"),
                output_field=models.DecimalField(
                    max_digits=10, decimal_places=2
                ),
            )
        )["total_price"] or Decimal("0.00")

        return total_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def get_total_quantity(self) -> int:
        """Return the cart total quantity.

        Returns:
            Decimal: Cart total quantity.
        """
        return (
            self.cart_items.aggregate(total_quantity=models.Sum("quantity"))[
                "total_quantity"
            ]
            or 0  # noqa: W503
        )

    def __str__(self) -> str:
        """Return a string representation of the cart.

        Returns:
            str: Cart user.
        """
        return (
            f"{_('Cart')} "
            f"({self.user} - {self.get_cart_status_display().lower()})"
        )


class CartItem(models.Model):
    """Model representing a cart item.

    Attributes:
        cart (ForeignKey): The cart to whom the cart item belongs.
        product (ForeignKey): Product belonging to the cart item.
        quantity (PositiveIntegerField): Number of products in cart item.
        price_snapshot (DecimalField): Price of the product at the time
            it was added to the cart.
    """

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

    def save(self, **kwargs: Any) -> None:
        """Set price snapshot on creation if not already set.

        Args:
            **kwargs: Additional context passed to the base implementation.
        """
        if not self.price_snapshot:
            self.price_snapshot = self.product.get_final_price()
        super().save(**kwargs)

    def __str__(self) -> str:
        """Return a string representation of the cart item.

        Returns:
            str: Cart item details.
        """
        return f"{self.cart}: {self.product} x {self.quantity}"
