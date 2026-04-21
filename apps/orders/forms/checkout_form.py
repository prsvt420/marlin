from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.orders.choices import DeliveryMethod
from apps.orders.models import Order


class CheckoutForm(forms.ModelForm):

    def clean_delivery_address(self) -> str:
        delivery_method: str = self.cleaned_data["delivery_method"]
        delivery_address: str = self.cleaned_data["delivery_address"]

        if delivery_method == DeliveryMethod.COURIER and not delivery_address:
            raise ValidationError(_("The delivery address is required."))

        return delivery_address

    class Meta:
        model = Order
        fields = (
            "delivery_method",
            "delivery_address",
            "payment_method",
            "recipient_name",
            "recipient_email",
            "recipient_phone_number",
            "comment",
        )
        error_messages = {
            "recipient_email": {
                "max_length": _(
                    "The email must not be longer than 255 characters."
                ),
                "invalid": _(
                    "The email must be in the format user@example.com."
                ),
                "required": _("The email is required."),
            },
            "recipient_name": {
                "max_length": _(
                    "The name must not be longer than 255 characters."
                ),
                "required": _("The name is required."),
            },
            "recipient_phone_number": {
                "required": _("The phone number is required."),
            },
        }
