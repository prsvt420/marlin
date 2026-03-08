from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.carts.choices import CartStatus
from apps.core.models import BaseModel


class Cart(BaseModel):  # type: ignore
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="carts",
        verbose_name=_("user"),
    )
    cart_status = models.CharField(
        max_length=20,
        choices=CartStatus.choices,
        default=CartStatus.ACTIVE,
        verbose_name=_("cart status"),
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
        ordering = ("-updated_at",)

    def __str__(self) -> str:
        return (
            f"{_('Cart')} "
            f"({self.user} - {self.get_cart_status_display().lower()})"
        )

    @property
    def total_quantity(self) -> int:
        return self.cart_items.count()
