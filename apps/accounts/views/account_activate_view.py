from django.contrib import messages
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.accounts.exceptions import AccountActivationLinkError
from apps.accounts.services import UserService


class AccountActivateView(View):

    def get(
        self, request: HttpRequest, uidb64: str, token: str
    ) -> HttpResponse:
        try:
            UserService().account_activate(uidb64=uidb64, token=token)
            messages.success(
                request,
                _("The activation was successful! Sign in to your account."),
            )
        except AccountActivationLinkError:
            messages.error(
                request,
                _("The account activation link is invalid or expired."),
            )

        return redirect(to="accounts:signin")
