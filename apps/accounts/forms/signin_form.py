from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UsernameField,
)
from django.utils.translation import gettext_lazy as _


class SignInForm(AuthenticationForm):
    """Form for signing in."""

    username = UsernameField(
        required=True,
        label=_("Username"),
        error_messages={
            "required": _("The username is required."),
        },
    )
    password = forms.CharField(
        required=True,
        label=_("Password"),
        strip=False,
        error_messages={"required": _("The password is required.")},
    )
