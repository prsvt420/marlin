from django import forms
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField


class ContactForm(forms.Form):
    """Form for collecting user contact information and message.

    This form is used to gather details from users who want to
    get in touch, including their name, email address, phone number,
    subject of the inquiry, and message content.

    Attributes:
        full_name (CharField): Full name of the user.
        email (EmailField): User's email address.
        phone_number (CharField): User's phone number.
        subject (CharField): Subject or topic of the message.
        message (CharField): The main text body of the user's message.
    """

    full_name = forms.CharField(
        max_length=255,
        error_messages={
            "required": _("The full name is required."),
            "max_length": _(
                "The full name must not be longer than 255 characters."
            ),
        },
    )
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
    phone_number = PhoneNumberField(
        region="RU",
        error_messages={
            "required": _("The phone number is required."),
            "invalid": _(
                "The phone number must " "be in the format +7 (XXX) XXX-XX-XX."
            ),
        },
    )
    subject = forms.CharField(
        max_length=255,
        error_messages={
            "required": _("The subject is required."),
            "max_length": _(
                "The subject must not be longer than 255 characters."
            ),
        },
    )
    message = forms.CharField(
        widget=forms.Textarea,
        error_messages={
            "required": _("The message is required."),
        },
    )
