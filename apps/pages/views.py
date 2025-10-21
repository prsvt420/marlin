from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.pages.forms import ContactForm


class ContactView(FormView):
    """Handles displaying and processing the contact form.

    Renders the 'pages/contact.html' template with a ContactForm.
    On successful submission, redirects to the same contact page
    or a success page defined by 'success_url'.
    """

    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("pages:contact")
