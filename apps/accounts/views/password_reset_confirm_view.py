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

from apps.accounts.forms import SetPasswordForm
from apps.accounts.services import UserService


class PasswordResetConfirmView(SuccessMessageMixin, _PasswordResetConfirmView):
    form_class = SetPasswordForm
    template_name = "accounts/redesign/password_reset_confirm.html"
    success_message = _(
        "Your password has been updated. You can now sign"
        " in with your new credentials."
    )
    success_url = reverse_lazy(viewname="accounts:signin")

    def dispatch(
        self, request, *args, **kwargs
    ) -> Union[HttpResponseBase, HttpResponsePermanentRedirect]:
        response: HttpResponseBase = super().dispatch(request, *args, **kwargs)

        if isinstance(response, TemplateResponse) and not self.validlink:
            messages.error(
                request, _("The password reset link is invalid or expired.")
            )
            return redirect(to="accounts:signin")

        return response

    def form_valid(self, form: SetPasswordForm) -> HttpResponse:
        response: HttpResponse = super().form_valid(form=form)
        UserService().send_password_reset_complete_email(user=self.user)
        return response
