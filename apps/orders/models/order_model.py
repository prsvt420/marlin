from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from apps.carts.models import Cart
from apps.core.models import BaseModel
from apps.orders.choices import (
    DeliveryMethod,
    OrderStatus,
    PaymentMethod,
    PaymentStatus,
)


class Order(BaseModel):  # type: ignore
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name=_("user"),
    )
    cart = models.OneToOneField(
        to=Cart,
        on_delete=models.SET_NULL,
        related_name="order",
        verbose_name=_("cart"),
        null=True,
        blank=True,
    )
    order_status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        verbose_name=_("order status"),
    )
    delivery_method = models.CharField(
        max_length=20,
        choices=DeliveryMethod.choices,
        verbose_name=_("delivery method"),
    )
    delivery_address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("delivery address"),
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        verbose_name=_("payment status"),
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        verbose_name=_("payment method"),
    )
    comment = models.TextField(
        blank=True,
        verbose_name=_("comment"),
    )
    recipient_name = models.CharField(
        max_length=255,
        verbose_name=_("recipient name"),
    )
    recipient_email = models.EmailField(
        max_length=255,
        verbose_name=_("recipient email"),
    )
    recipient_phone_number = PhoneNumberField(
        region="RU",
        verbose_name=_("recipient phone number"),
        help_text="+7__________",
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        default=Decimal("0.00"),
        verbose_name=_("total price"),
        help_text=_("Calculated by the system."),
    )
    number = models.CharField(
        max_length=20,
        verbose_name=_("number"),
        unique=True,
        editable=False,
        help_text="ORD-0000-000000",
    )

    class Meta:  # noqa: D106
        db_table = "orders_order"
        db_table_comment = "Table containing orders."
        verbose_name = _("order")
        verbose_name_plural = _("orders")
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return (
            f"{_('Order')} {self.number} "
            f"({self.get_order_status_display().lower()})"
        )

    @property
    def total_quantity(self) -> int:
        return self.order_items.count()
