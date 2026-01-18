from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import (
    LoginView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.http import (
    HttpResponse,
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ipware import get_client_ip

from apps.accounts.email_templates import (
    SIGNIN_NOTIFICATION,
)
from apps.accounts.forms import SignInForm
from apps.core.services import EmailService


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
