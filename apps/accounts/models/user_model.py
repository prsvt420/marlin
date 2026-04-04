from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy
from phonenumber_field.modelfields import PhoneNumberField

from apps.accounts.managers import UserManager


class User(AbstractUser):
    objects = UserManager()  # type: ignore
    username = None  # type: ignore
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name=_("email"),
    )
    phone_number = PhoneNumberField(
        blank=True,
        null=True,
        unique=True,
        region="RU",
        verbose_name=_("phone number"),
        help_text="+7__________",
    )
    first_name = models.CharField(
        max_length=255,
        verbose_name=_("first name"),
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name=_("last name"),
    )
    middle_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("middle name"),
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name=pgettext_lazy("masculine", "active"),
    )
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]
    USERNAME_FIELD = "email"

    class Meta:
        db_table = "accounts_user"
        db_table_comment = "Table containing users."
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ("-date_joined",)

    @property
    def full_name(self) -> str:
        full_name: str = "%s %s %s" % (
            self.last_name,
            self.first_name,
            self.middle_name,
        )
        return full_name.strip()
