from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import (
    HttpResponse,
)
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from apps.accounts.forms import SignUpForm
from apps.accounts.services import UserService
from apps.core.services import YandexSmartCaptchaService
from config.settings import YANDEX_SMART_CAPTCHA_CLIENT_KEY


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = "accounts/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy(viewname="accounts:signin")
    success_message = _(
        "You have successfully signed up! Activate your account."
    )
    extra_context = {
        "YANDEX_SMART_CAPTCHA_CLIENT_KEY": YANDEX_SMART_CAPTCHA_CLIENT_KEY
    }

    def form_valid(self, form: SignUpForm) -> HttpResponse:
        if not YandexSmartCaptchaService().validate_captcha(
            request=self.request
        ):
            messages.error(
                self.request,
                _("Please pass the captcha and try again."),
            )
            form.add_error(None, _("Please pass the captcha and try again."))
            return super().form_invalid(form=form)

        response: HttpResponse = super().form_valid(form=form)

        UserService().send_account_activation_email(
            user=self.object  # type: ignore
        )
        messages.info(
            self.request,
            _("An account activation link has been sent to your email."),
        )

        return response

    def form_invalid(self, form: SignUpForm) -> HttpResponse:
        messages.error(
            self.request,
            _("Please correct the errors in the form and try again."),
        )
        return super().form_invalid(form=form)
