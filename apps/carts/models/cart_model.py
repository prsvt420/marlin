from decimal import ROUND_HALF_UP, Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.carts.choices import CartStatus


class Cart(models.Model):
    """Model for cart."""

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

    def __str__(self) -> str:  # noqa: D105
        return (
            f"{_('Cart')} "
            f"({self.user} - {self.get_cart_status_display().lower()})"
        )

    def get_total_price(self) -> Decimal:
        """Return the cart total price."""
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
        """Return the cart total quantity."""
        return self.cart_items.count()
