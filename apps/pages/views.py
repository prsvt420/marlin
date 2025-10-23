from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.pages.forms import ContactForm
from apps.pages.services.email_service import EmailService
from apps.pages.types import ContactContext


class ContactView(FormView):
    """Handles displaying and processing the contact form.

    Renders the 'pages/contact.html' template with a ContactForm.
    On successful submission, redirects to the same contact page
    or a success page defined by 'success_url'.
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

        email_service: EmailService = EmailService()
        email_service.send_contact_message(contact_context=contact_context)
        email_service.send_contact_reply(contact_context=contact_context)

        return super().form_valid(form)
