from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """Model for user."""

    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name=_("email"),
        help_text=_("User email."),
    )
    phone_number = PhoneNumberField(
        unique=True,
        verbose_name=_("phone number"),
        help_text=_("User phone number."),
        region="RU",
    )
    first_name = models.CharField(
        verbose_name=_("first name"),
        max_length=255,
        help_text=_("User first name."),
    )
    last_name = models.CharField(
        verbose_name=_("last name"),
        max_length=255,
        help_text=_("User last name."),
    )
    middle_name = models.CharField(
        verbose_name=_("middle name"),
        max_length=255,
        help_text=_("User middle name."),
        blank=True,
    )
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    REQUIRED_FIELDS = [
        "email",
        "phone_number",
        "first_name",
        "last_name",
        "middle_name",
    ]

    class Meta:  # noqa: D106
        db_table = "accounts_user"
        db_table_comment = "Table containing users."
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ("-date_joined",)
