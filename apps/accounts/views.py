from typing import Any, Dict, Optional, Union

from django.contrib import messages
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.contrib.auth.views import (
    PasswordResetConfirmView as _PasswordResetConfirmView,
)
from django.contrib.auth.views import PasswordResetView as _PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBase,
    HttpResponsePermanentRedirect,
)
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import CreateView
from ipware import get_client_ip

from apps.accounts.email_templates import (
    ACCOUNT_ACTIVATION,
    PASSWORD_RESET_COMPLETE,
    SIGNIN_NOTIFICATION,
)
from apps.accounts.forms import (
    PasswordResetForm,
    SetPasswordForm,
    SignInForm,
    SignUpForm,
)
from apps.accounts.repositories.user_repository import UserRepository
from apps.core.services.email_service import EmailService


class SignInView(SuccessMessageMixin, LoginView):
    """View for handling the sign in form."""

    template_name = "accounts/signin.html"
    success_message = _("You have successfully signed in. Welcome!")
    redirect_authenticated_user = True
    form_class = SignInForm

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        """Handle a valid sign in form and send notification email."""
        context = {
            "date": timezone.localtime(timezone.now()),
            "client_ip": get_client_ip(self.request)[0],
            "user_agent": self.request.user_agent,  # type: ignore
        }

        try:
            email_service: EmailService = EmailService()
            email_service.send_email(
                email_template=SIGNIN_NOTIFICATION,
                to=[form.get_user().email],  # type: ignore
                context=context,
            )
        except Exception:  # noqa: S110
            pass

        return super().form_valid(form=form)

    def form_invalid(self, form: AuthenticationForm) -> HttpResponse:
        """Handle an invalid sign in form and display an error message."""
        messages.error(
            self.request,
            _("Please correct the errors in the form and try again."),
        )
        return super().form_invalid(form)


class SignOutView(LogoutView):
    """View for handling the sign out."""

    def get_redirect_url(self) -> str:
        """Add a success message and return the logout redirect URL."""
        messages.success(
            self.request, _("You have been signed out. Have a nice day!")
        )
        return super().get_redirect_url()


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


class PasswordResetView(SuccessMessageMixin, _PasswordResetView):
    """View for handling the password reset form."""

    template_name = "accounts/password_reset.html"
    email_template_name = "emails/password_reset.txt"
    subject_template_name = "emails/password_reset_subject.txt"
    html_email_template_name = "emails/password_reset.html"
    success_message = _("A password reset link has been sent to your email.")
    success_url = reverse_lazy("accounts:signin")
    form_class = PasswordResetForm


class PasswordResetConfirmView(SuccessMessageMixin, _PasswordResetConfirmView):
    """View for handling the set password form."""

    form_class = SetPasswordForm
    template_name = "accounts/password_reset_confirm.html"
    success_message = _(
        "Your password has been updated. You can now sign"
        " in with your new credentials."
    )
    success_url = reverse_lazy("accounts:signin")

    def dispatch(
        self, request, *args, **kwargs
    ) -> Union[HttpResponseBase, HttpResponsePermanentRedirect]:
        """Handle invalid or expired password reset links and redirect."""
        response: HttpResponseBase = super().dispatch(request, *args, **kwargs)

        if isinstance(response, TemplateResponse) and not self.validlink:
            messages.error(
                request, _("The password reset link is invalid or expired.")
            )
            return redirect("accounts:signin")

        return response

    def form_valid(self, form: SetPasswordForm) -> HttpResponse:
        """Handle a valid set password form and send notification email."""
        try:
            email_service: EmailService = EmailService()
            email_service.send_email(
                email_template=PASSWORD_RESET_COMPLETE,
                to=[self.user.email],
            )
        except Exception:  # noqa: S110
            pass

        return super().form_valid(form=form)


class AccountActivationView(View):
    """View for activating the user account."""

    token_generator = default_token_generator

    def get(self, request: HttpRequest, token: str, uidb64: str):
        """Activate the user if the token is valid and redirect to sign in."""
        user: Optional[AbstractBaseUser]

        try:
            user_pk: str = force_str(urlsafe_base64_decode(uidb64))
            user = UserRepository.get_by_pk(pk=user_pk)
        except Exception:  # noqa: S110
            user = None

        if user is not None and self.token_generator.check_token(user, token):
            UserRepository.activate(user=user)
            messages.success(
                request,
                _("The activation was successful! Sign in to your account."),
            )
        else:
            messages.error(
                request,
                _("The account activation link is invalid or expired."),
            )

        return redirect("accounts:signin")
