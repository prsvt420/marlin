from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
)
from django.utils.translation import gettext_lazy as _


class SignInForm(AuthenticationForm):
    username = forms.EmailField(
        required=True,
        label=_("Email"),
        error_messages={
            "required": _("The email is required."),
        },
    )
    password = forms.CharField(
        required=True,
        label=_("Password"),
        strip=False,
        error_messages={"required": _("The password is required.")},
    )
