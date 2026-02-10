from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from apps.pages.exceptions import ContactInboundEmailSendError
from apps.pages.forms import ContactForm
from apps.pages.services import ContactService


class ContactView(FormView):

    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy(viewname="pages:contact")

    def form_valid(self, form: ContactForm) -> HttpResponse:
        try:
            ContactService().send_contact_emails(context=form.cleaned_data)
            messages.success(
                request=self.request,
                message=_(
                    "Your message has been successfully sent! "
                    "We will contact you shortly."
                ),
            )
        except ContactInboundEmailSendError:
            messages.error(
                self.request,
                _(
                    "An error occurred while sending your message. "
                    "Please try again later."
                ),
            )
        return super().form_valid(form=form)

    def form_invalid(self, form: ContactForm) -> HttpResponse:
        messages.error(
            self.request,
            _("Please correct the errors in the form and try again."),
        )
        return super().form_invalid(form=form)
