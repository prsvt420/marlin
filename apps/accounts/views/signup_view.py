from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import (
    HttpResponse,
)
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from apps.accounts.exceptions import AccountActivationEmailSendError
from apps.accounts.forms import SignUpForm
from apps.accounts.services import UserService


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = "accounts/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy(viewname="accounts:signin")
    success_message = _(
        "You have successfully signed up! Activate your account."
    )

    def form_valid(self, form: SignUpForm) -> HttpResponse:
        response: HttpResponse = super().form_valid(form=form)

        try:
            UserService().send_account_activation_email(
                user=self.object  # type: ignore
            )
            messages.info(
                self.request,
                _("An account activation link has been sent to your email."),
            )
        except AccountActivationEmailSendError:
            messages.error(
                self.request,
                _(
                    "An error occurred while sending the account "
                    "activation link. Please try again later."
                ),
            )

        return response

    def form_invalid(self, form: SignUpForm) -> HttpResponse:
        messages.error(
            self.request,
            _("Please correct the errors in the form and try again."),
        )
        return super().form_invalid(form=form)
