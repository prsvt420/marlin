from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from apps.core.services import YandexSmartCaptchaService
from apps.pages.forms import ContactForm
from apps.pages.services import ContactService
from config.settings import YANDEX_SMART_CAPTCHA_CLIENT_KEY


class ContactView(FormView):
    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy(viewname="pages:contact")
    extra_context = {
        "YANDEX_SMART_CAPTCHA_CLIENT_KEY": YANDEX_SMART_CAPTCHA_CLIENT_KEY,
        "breadcrumbs": [
            {"name": _("Home"), "url": reverse_lazy(viewname="pages:home")},
            {
                "name": _("Contacts"),
                "url": reverse_lazy(viewname="pages:contact"),
            },
        ],
    }

    def form_valid(self, form: ContactForm) -> HttpResponse:
        if not YandexSmartCaptchaService().validate_captcha(
            request=self.request
        ):
            messages.error(
                self.request,
                _("Please pass the captcha and try again."),
            )
            return super().form_invalid(form=form)

        ContactService().send_contact_emails(context=form.cleaned_data)
        messages.success(
            request=self.request,
            message=_(
                "Your message has been successfully sent! "
                "We will contact you shortly."
            ),
        )

        return super().form_valid(form=form)

    def form_invalid(self, form: ContactForm) -> HttpResponse:
        messages.error(
            self.request,
            _("Please correct the errors in the form and try again."),
        )
        return super().form_invalid(form=form)
