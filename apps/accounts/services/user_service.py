from typing import Any, Mapping, Optional

from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.http import HttpRequest
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from ipware import get_client_ip

from apps.accounts.email_templates import (
    ACCOUNT_ACTIVATION_EMAIL,
    PASSWORD_RESET_COMPLETE_EMAIL,
    SIGNIN_NOTIFICATION_EMAIL,
)
from apps.accounts.exceptions import (
    AccountActivationEmailSendError,
    AccountActivationLinkError,
)
from apps.accounts.models import User
from apps.accounts.selectors import UserSelector
from apps.core.exceptions import EmailSendError
from apps.core.services import EmailService


class UserService:

    def __init__(self) -> None:
        self._email_service: EmailService = EmailService()

    def account_activate(self, *, uidb64: str, token: str) -> None:
        try:
            user_pk: int = int(force_str(s=urlsafe_base64_decode(s=uidb64)))
        except ValueError as error:
            raise AccountActivationLinkError(
                "The account activation link is invalid"
            ) from error

        user: Optional[User] = UserSelector().get_user(user_pk=user_pk)

        if user is None or not default_token_generator.check_token(
            user=user, token=token
        ):
            raise AccountActivationLinkError(
                "The account activation link is invalid or expired"
            )

        if not user.is_active:
            with transaction.atomic():
                user.is_active = True
                user.save(update_fields=["is_active"])

    def send_account_activation_email(self, *, user: User):
        context: Mapping[str, Any] = {
            "token": default_token_generator.make_token(user=user),
            "uid": urlsafe_base64_encode(s=force_bytes(s=user.pk)),
        }

        try:
            self._email_service.send_email(
                email_template=ACCOUNT_ACTIVATION_EMAIL,
                to=[user.email],  # type: ignore
                context=context,
            )
        except EmailSendError as error:
            raise AccountActivationEmailSendError(
                "Couldn't send a account activation email"
            ) from error

    def send_signin_notification_email(
        self, *, request: HttpRequest, user: User
    ) -> None:
        context: Mapping[str, Any] = {
            "date": timezone.localtime(value=timezone.now()),
            "client_ip": get_client_ip(request=request)[0],
            "user_agent": getattr(
                request,
                "user_agent",
                "Unknown",
            ),
        }

        try:
            self._email_service.send_email(
                email_template=SIGNIN_NOTIFICATION_EMAIL,
                to=[user.email],
                context=context,
            )
        except EmailSendError:  # noqa: S110
            pass

    def send_password_reset_complete_email(self, *, user: User) -> None:
        try:
            self._email_service.send_email(
                email_template=PASSWORD_RESET_COMPLETE_EMAIL,
                to=[user.email],
            )
        except EmailSendError:  # noqa: S110
            pass
