from django import forms
from django.contrib.auth.forms import PasswordResetForm as _PasswordResetForm
from django.utils.translation import gettext_lazy as _


class PasswordResetForm(_PasswordResetForm):
    email = forms.EmailField(
        max_length=255,
        error_messages={
            "required": _("The email is required."),
            "invalid": _("The email must be in the format user@example.com."),
            "max_length": _(
                "The email must not be longer than 255 characters."
            ),
        },
    )
