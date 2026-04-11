from typing import Optional

from django.contrib import messages
from django.contrib.auth.views import PasswordResetView as _PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from apps.accounts.forms import PasswordResetForm
from apps.accounts.models import User
from apps.accounts.selectors import UserSelector
from apps.core.services import YandexSmartCaptchaService
from config.settings import YANDEX_SMART_CAPTCHA_CLIENT_KEY


class PasswordResetView(SuccessMessageMixin, _PasswordResetView):
    template_name = "accounts/redesign/password_reset.html"
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
            form.add_error(None, _("Please pass the captcha and try again."))
            return super().form_invalid(form=form)

        user: Optional[User] = UserSelector().get_user_by_email(
            email=form.cleaned_data["email"]
        )

        if user and not UserSelector().has_usable_password(user=user):
            messages.error(
                self.request,
                _(
                    "This account uses social sign in. Please "
                    "sign in with social account and set a password."
                ),
            )
            return redirect(to="accounts:signin")

        return super().form_valid(form=form)

    def form_invalid(self, form: PasswordResetForm) -> HttpResponse:
        messages.error(
            self.request,
            _("Please correct the errors in the form and try again."),
        )
        return super().form_invalid(form=form)
