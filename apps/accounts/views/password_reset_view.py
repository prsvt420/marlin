from django.contrib import messages
from django.contrib.auth.views import PasswordResetView as _PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from apps.accounts.forms import PasswordResetForm
from apps.core.services import YandexSmartCaptchaService
from config.settings import YANDEX_SMART_CAPTCHA_CLIENT_KEY


class PasswordResetView(SuccessMessageMixin, _PasswordResetView):
    template_name = "accounts/password_reset.html"
    email_template_name = "emails/password_reset.txt"
    subject_template_name = "emails/password_reset_subject.txt"
    html_email_template_name = "emails/password_reset.html"
    success_message = _("A password reset link has been sent to your email.")
    success_url = reverse_lazy(viewname="accounts:signin")
    form_class = PasswordResetForm
    extra_context = {
        "YANDEX_SMART_CAPTCHA_CLIENT_KEY": YANDEX_SMART_CAPTCHA_CLIENT_KEY
    }

    def form_valid(self, form: PasswordResetForm) -> HttpResponse:
        if not YandexSmartCaptchaService().validate_captcha(
            request=self.request
        ):
            messages.error(
                self.request,
                _("Please pass the captcha and try again."),
            )
            return super().form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form: PasswordResetForm) -> HttpResponse:
        messages.error(
            self.request,
            _("Please correct the errors in the form and try again."),
        )
        return super().form_invalid(form)
