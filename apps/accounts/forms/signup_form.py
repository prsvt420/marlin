from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
)
from django.utils.translation import gettext_lazy as _


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        required=True,
        strip=False,
        error_messages={"required": _("The password is required.")},
    )
    password2 = forms.CharField(
        required=True,
        strip=False,
        error_messages={
            "required": _("The password confirmation is required.")
        },
    )
    agreement = forms.BooleanField(
        required=True,
        error_messages={"required": _("Consent required.")},
    )

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "first_name",
            "last_name",
            "middle_name",
        )
        error_messages = {
            "email": {
                "max_length": _(
                    "The email must not be longer than 255 characters."
                ),
                "invalid": _(
                    "The email must be in the format user@example.com."
                ),
                "unique": _("This email address is already registered."),
                "required": _("The email is required."),
            },
            "first_name": {
                "max_length": _(
                    "The first name must not be longer than 255 characters."
                ),
                "required": _("The first name is required."),
            },
            "last_name": {
                "max_length": _(
                    "The last name must not be longer than 255 characters."
                ),
                "required": _("The last name is required."),
            },
            "middle_name": {
                "max_length": _(
                    "The middle name must not be longer than 255 characters."
                )
            },
        }
