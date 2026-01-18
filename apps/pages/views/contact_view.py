from typing import Dict

from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from apps.core.services import EmailService
from apps.pages.email_templates import CONTACT_MESSAGE, CONTACT_REPLY
from apps.pages.forms import ContactForm
from config import settings


class ContactView(FormView):
    """View for handling the contact form."""

    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("pages:contact")

    def form_valid(self, form: ContactForm) -> HttpResponse:
        """Handle a valid contact form and send notification emails."""
        context: Dict[str, str] = {
            "full_name": form.cleaned_data["full_name"],
            "email": form.cleaned_data["email"],
            "phone_number": form.cleaned_data["phone_number"],
            "subject": form.cleaned_data["subject"],
            "message": form.cleaned_data["message"],
        }

        try:
            email_service: EmailService = EmailService()
            email_service.send_email(
                email_template=CONTACT_MESSAGE,
                to=[settings.DEFAULT_FROM_EMAIL],
                context=context,
            )
            email_service.send_email(
                email_template=CONTACT_REPLY,
                to=[context["email"]],
                context=context,
            )

            messages.success(
                request=self.request,
                message=_(
                    "Your message has been successfully sent! "
                    "We will contact you shortly."
                ),
            )
        except Exception:
            messages.error(
                self.request,
                _(
                    "An error occurred while sending your message. "
                    "Please try again later."
                ),
            )

        return super().form_valid(form=form)

    def form_invalid(self, form: ContactForm) -> HttpResponse:
        """Handle an invalid contact form and display an error message."""
        messages.error(
            self.request,
            _("Please correct the errors in the form and try again."),
        )
        return super().form_invalid(form=form)
