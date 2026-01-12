from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
)
from django.contrib.auth.forms import PasswordResetForm as _PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm as _SetPasswordForm
from django.contrib.auth.forms import (
    UserCreationForm,
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


class SignUpForm(UserCreationForm):
    """Form for signing up."""

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

    class Meta:  # noqa: D106
        model = get_user_model()
        fields = (
            "username",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "middle_name",
        )
        error_messages = {
            "username": {
                "max_length": _(
                    "The username must not be longer than 255 characters."
                ),
                "unique": _("This username is already in use."),
                "required": _("The username is required."),
            },
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
            "phone_number": {
                "invalid": _(
                    "The phone number must "
                    "be in the format +7 (XXX) XXX-XX-XX."
                ),
                "unique": _("This phone number is already registered."),
                "required": _("The phone number is required."),
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


class PasswordResetForm(_PasswordResetForm):
    """Form for requesting a password reset."""

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
