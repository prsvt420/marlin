from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """Model representing a user in the system.

    This model extends Django's built-in AbstractUser and adds additional
    fields.

    Each record stores information about a single user, including
    authentication data, contact information, and personal details.

    Attributes:
        username (CharField): User's username.
        email (EmailField): User's email.
        phone_number (PhoneNumberField): User's phone number.
        first_name (CharField): User's first name.
        last_name (CharField): User's last name.
        middle_name (CharField): User's middle name.
        password (CharField): Hashed password.
        is_staff (BooleanField): Determines if the user can access the
            admin site.
        is_active (BooleanField): Determines if the user account is active.
        is_superuser (BooleanField): Determines if the user has all
            permissions.
        last_login (DateTimeField): Date and time of the user's last login.
        date_joined (DateTimeField): Date and time of the user's
            account creation.
    """

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

    REQUIRED_FIELDS = [
        "email",
        "phone_number",
        "first_name",
        "last_name",
        "middle_name",
    ]

    class Meta:  # noqa: D106
        db_table_comment = "Table containing users."
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ("-date_joined",)
