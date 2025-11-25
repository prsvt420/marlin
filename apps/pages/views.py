from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, RedirectView, TemplateView

from apps.pages.forms import ContactForm
from apps.pages.services.email_service import EmailService
from apps.pages.types import ContactContext


class ContactView(FormView):
    """Handles displaying and processing the contact form.

    Renders the `pages/contact.html` template with a ContactForm.
    On successful submission, redirects to the same contact page
    or a success page defined by `success_url`.
    """

    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("pages:contact")

    def form_valid(self, form: ContactForm) -> HttpResponse:
        """Process the contact form and send emails.

        Extracts cleaned data from the submitted form and constructs
        a ContactContext dictionary. Sends the contact message to
        the email service and sends a reply to the sender.

        Args:
            form (ContactForm): The submitted contact form instance.

        Returns:
            HttpResponse: The HTTP response returned by the parent class's
            form_valid method.
        """
        contact_context: ContactContext = {
            "name": form.cleaned_data["name"],
            "email": form.cleaned_data["email"],
            "phone": form.cleaned_data["phone"],
            "subject": form.cleaned_data["subject"],
            "message": form.cleaned_data["message"],
        }

        try:
            email_service: EmailService = EmailService()
            email_service.send_contact_message(contact_context=contact_context)
            email_service.send_contact_reply(contact_context=contact_context)

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
        """Handle invalid form submission.

        Displays an error message to the user when the contact form
        contains validation errors. The message informs the user to
        correct the errors and try again.

        Args:
            form (ContactForm): The invalid contact form
            instance with validation errors.

        Returns:
            HttpResponse: The HTTP response returned by the parent class's
            form_invalid method, which re-renders the form with error messages.
        """
        messages.error(
            self.request,
            _("Please correct the errors in the form and try again."),
        )
        return super().form_invalid(form=form)


class PrivacyView(TemplateView):
    """Displays the privacy policy page.

    Uses the `pages/privacy.html` template to render
    the privacy policy and data handling information.
    """

    template_name = "pages/privacy.html"


class TermsView(TemplateView):
    """Displays the terms of service page.

    Uses the `pages/terms.html` template to render
    the terms and conditions for using the service.
    """

    template_name = "pages/terms.html"


class OfferView(TemplateView):
    """Displays the public offer agreement page.

    Uses the `pages/offer.html` template to render
    the public offer agreement and contract terms.
    """

    template_name = "pages/offer.html"


class CatalogRedirectView(RedirectView):
    """Permanent redirection to the catalog page.

    Redirects the user to the `catalog:category_list`
    page with HTTP code 301.
    """

    pattern_name = "catalog:category_list"
    permanent = True
