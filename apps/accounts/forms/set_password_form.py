from django import forms
from django.contrib.auth.forms import SetPasswordForm as _SetPasswordForm
from django.utils.translation import gettext_lazy as _


class SetPasswordForm(_SetPasswordForm):
    """Form for setting a new password."""

    new_password1 = forms.CharField(
        required=True,
        strip=False,
        error_messages={"required": _("The new password is required.")},
    )
    new_password2 = forms.CharField(
        required=True,
        strip=False,
        error_messages={
            "required": _("The new password confirmation is required.")
        },
    )
