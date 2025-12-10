from typing import Union

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.contrib.auth.views import (
    PasswordResetConfirmView as _PasswordResetConfirmView,
)
from django.contrib.auth.views import PasswordResetView as _PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMultiAlternatives
from django.http import (
    HttpResponse,
    HttpResponseBase,
    HttpResponsePermanentRedirect,
)
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from apps.accounts.forms import PasswordResetForm, SetPasswordForm, SignUpForm


class SignInView(SuccessMessageMixin, LoginView):
    """Displays the sign in page.

    Renders the `accounts/signin.html` template with a AuthenticationForm.
    """

    template_name = "accounts/signin.html"
    success_message = _("You have successfully signed in. Welcome!")
    redirect_authenticated_user = True

    def form_invalid(self, form: AuthenticationForm) -> HttpResponse:
        """Handle invalid form submission.

        Displays an error message to the user when the sign in form
        contains validation errors. The message in forms the user to
        correct the errors and try again.

        Args:
            form (AuthenticationForm): The invalid sign in form
            instance with validation errors.

        Returns:
            HttpResponse: The HTTP response returned by the parent class's
            form_invalid method, which re-renders the form with error messages.
        """
        messages.error(
            self.request,
            _("Please correct the errors in the form and try again."),
        )
        return super().form_invalid(form)


class SignOutView(LogoutView):
    """Handles user sign out functionality.

    Extends Django's LogoutView to provide custom success message
    feedback to users upon successful logout.
    """

    def get_redirect_url(self) -> str:
        """Process logout redirect with success message.

        Displays a success message confirming the logout operation
        before redirecting the user to the appropriate URL.

        Returns:
            str: The redirect URL returned by the parent class's
            get_redirect_url method, typically the homepage or
            login page.
        """
        messages.success(
            self.request, _("You have been signed out. Have a nice day!")
        )
        return super().get_redirect_url()


class SignUpView(SuccessMessageMixin, CreateView):
    """Displays the sign up page.

    Renders the `accounts/signup.html` template with a SignUpForm.
    """

    template_name = "accounts/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("accounts:signin")
    success_message = _(
        "You have successfully signed up! Sign in to your account."
    )

    def form_invalid(self, form: SignUpForm) -> HttpResponse:
        """Handle invalid form submission.

        Displays an error message to the user when the sign up form
        contains validation errors. The message in forms the user to
        correct the errors and try again.

        Args:
            form (SignUpForm): The invalid sign up form
            instance with validation errors.

        Returns:
            HttpResponse: The HTTP response returned by the parent class's
            form_invalid method, which re-renders the form with error messages.
        """
        messages.error(
            self.request,
            _("Please correct the errors in the form and try again."),
        )
        return super().form_invalid(form)


class PasswordResetView(SuccessMessageMixin, _PasswordResetView):
    """Displays the password reset request page.

    Renders the `accounts/password_reset.html` template with
    a PasswordResetForm.
    """

    template_name = "accounts/password_reset.html"
    email_template_name = "emails/password_reset.txt"
    subject_template_name = "emails/password_reset_subject.txt"
    html_email_template_name = "emails/password_reset.html"
    success_message = _("A password reset link has been sent to your email.")
    success_url = reverse_lazy("accounts:signin")
    form_class = PasswordResetForm


class PasswordResetConfirmView(SuccessMessageMixin, _PasswordResetConfirmView):
    """Displays the password reset confirmation page.

    Renders the `accounts/password_reset_confirm.html` template with
    a SetPasswordForm.
    """

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
        """Validate password reset link before processing the request.

        Checks whether the password reset link provided in the URL is valid.
        If the link is invalid or expired, an error message is displayed
        to the user and they are redirected to the sign-in page.
        Otherwise, continues with the standard dispatch flow.

        Returns:
            Union[HttpResponseBase, HttpResponsePermanentRedirect]:
                - A redirect response to the sign-in page if
                the link is invalid.
                - Otherwise, the standard dispatch response
                from the parent class.
        """
        response: HttpResponseBase = super().dispatch(request, *args, **kwargs)

        if isinstance(response, TemplateResponse) and not self.validlink:
            messages.error(
                request, _("The password reset link is invalid or expired.")
            )
            return redirect("accounts:signin")

        return response

    def form_valid(self, form: SetPasswordForm) -> HttpResponse:
        """Process password reset confirmation and send notification emails.

        Args:
            form (SetPasswordForm): The submitted set password form instance.

        Returns:
            HttpResponse: The HTTP response returned by the parent class's
            form_valid method.
        """
        body: str = render_to_string(
            "emails/password_reset_complete.txt",
        )
        content: str = render_to_string(
            template_name="emails/password_reset_complete.html",
        )
        subject: str = render_to_string(
            "emails/password_reset_complete_subject.txt",
        ).strip()

        email_message: EmailMultiAlternatives = EmailMultiAlternatives(
            subject=subject,
            body=body,
            to=[self.user.email],
        )
        email_message.attach_alternative(content=content, mimetype="text/html")

        email_message.send()

        return super().form_valid(form=form)
