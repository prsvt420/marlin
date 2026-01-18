from typing import Union

from django.contrib import messages
from django.contrib.auth.views import (
    PasswordResetConfirmView as _PasswordResetConfirmView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.http import (
    HttpResponse,
    HttpResponseBase,
    HttpResponsePermanentRedirect,
)
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from apps.accounts.email_templates import (
    PASSWORD_RESET_COMPLETE,
)
from apps.accounts.forms import SetPasswordForm
from apps.core.services import EmailService


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
