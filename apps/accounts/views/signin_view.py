from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import (
    LoginView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.http import (
    HttpResponse,
)
from django.utils.translation import gettext_lazy as _

from apps.accounts.forms import SignInForm
from apps.accounts.services import UserService


class SignInView(SuccessMessageMixin, LoginView):
    template_name = "accounts/redesign/signin.html"
    success_message = _("You have successfully signed in. Welcome!")
    redirect_authenticated_user = True
    form_class = SignInForm

    def form_valid(self, form: AuthenticationForm) -> HttpResponse:
        response: HttpResponse = super().form_valid(form=form)
        UserService().send_signin_notification_email(
            request=self.request, user=form.get_user()  # type: ignore
        )
        return response

    def form_invalid(self, form: AuthenticationForm) -> HttpResponse:
        messages.error(
            self.request,
            _("Please correct the errors in the form and try again."),
        )
        return super().form_invalid(form=form)
