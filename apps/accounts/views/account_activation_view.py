from typing import Optional

from django.contrib import messages
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import default_token_generator
from django.http import (
    HttpRequest,
)
from django.shortcuts import redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.accounts.repositories import UserRepository


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
