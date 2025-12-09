from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm as _PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm as _SetPasswordForm
from django.contrib.auth.forms import (
    UserCreationForm,
)
from django.utils.translation import gettext_lazy as _


class SignUpForm(UserCreationForm):
    """Form for registering a new user with detailed personal information.

    This form extends Django's built-in UserCreationForm and adds additional
    fields.

    This form is used to create a new user account, including
    username, email, phone number, and full name details. It also
    handles password creation and validation.

    Attributes:
        username (CharField): User's username.
        email (EmailField): User's email address.
        phone_number (CharField): User's phone number.
        first_name (CharField): User's first name.
        last_name (CharField): User's last name.
        middle_name (CharField): User's middle name.
        password1 (CharField): Password for the new account.
        password2 (CharField): Password confirmation to verify accuracy.
    """

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
    """Form for requesting a password reset by email.

    This form extends Django's built-in PasswordResetForm.

    Attributes:
        email (EmailField): User's email address.
    """

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
    """Form for setting a new password after a password reset request.

    This form extends Django's built-in SetPasswordForm.

    Attributes:
        new_password1 (CharField): New password.
        new_password2 (CharField): New password confirmation
        to verify accuracy.
    """

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
