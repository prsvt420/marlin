from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from django_stubs_ext import StrOrPromise

from apps.carts.choices import CartStatus


class Cart(models.Model):  # type: ignore
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

    def __str__(self) -> str:
        return (
            f"{_('Cart')} "
            f"({self.user} - {self.get_cart_status_display().lower()})"
        )

    @property
    def total_quantity(self) -> int:
        return self.cart_items.count()

    @property
    def formatted_total_quantity(self) -> StrOrPromise:
        total_quantity: int = self.total_quantity
        formatted_total_quantity: StrOrPromise = ngettext(
            "%(total_quantity)s product",
            "%(total_quantity)s products",
            total_quantity,
        )

        return formatted_total_quantity % {"total_quantity": total_quantity}
