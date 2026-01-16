from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.http import (
    HttpResponse,
)
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from apps.accounts.email_templates import (
    ACCOUNT_ACTIVATION,
)
from apps.accounts.forms import SignUpForm
from apps.core.services.email_service import EmailService


class SignUpView(SuccessMessageMixin, CreateView):
    """View for handling the sign up form."""

    template_name = "accounts/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("accounts:signin")
    success_message = _(
        "You have successfully signed up! Activate your account."
    )
    token_generator = default_token_generator

    def form_valid(self, form: SignUpForm) -> HttpResponse:
        """Handle a valid sign up form and send activation email."""
        response: HttpResponse = super().form_valid(form)

        try:
            user: AbstractBaseUser = self.object  # type: ignore
            token: str = self.token_generator.make_token(user)
            uid: str = urlsafe_base64_encode(force_bytes(user.pk))

            context: Dict[str, Any] = {
                "token": token,
                "uid": uid,
            }

            email_service: EmailService = EmailService()
            email_service.send_email(
                email_template=ACCOUNT_ACTIVATION,
                to=[user.email],  # type: ignore
                context=context,
            )
            messages.info(
                self.request,
                _("An account activation link has been sent to your email."),
            )
        except Exception:
            messages.error(
                self.request,
                _(
                    "An error occurred while sending the account "
                    "activation link. Please try again later."
                ),
            )

        return response

    def form_invalid(self, form: SignUpForm) -> HttpResponse:
        """Handle an invalid sign up form and display an error message."""
        messages.error(
            self.request,
            _("Please correct the errors in the form and try again."),
        )
        return super().form_invalid(form)
