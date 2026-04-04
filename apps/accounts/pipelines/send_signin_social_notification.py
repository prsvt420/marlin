from typing import Any, Dict, Optional

from django.contrib import messages
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from social_core.backends.base import BaseAuth
from social_core.storage import UserProtocol

from apps.accounts.services import UserService


def send_signin_social_notification(
    backend: BaseAuth,
    request: HttpRequest,
    user: Optional[UserProtocol] = None,
    **kwargs: Any,
) -> None:
    if not user:
        return

    backends: Dict[str, str] = {
        "google-oauth2": "Google",
    }

    backend_name: str = backends.get(backend.name, backend.name)

    UserService().send_signin_notification_email(
        request=request, user=user  # type: ignore
    )
    messages.success(
        request,
        _("You have successfully signed in with %(backend_name)s. Welcome!")
        % {"backend_name": backend_name},
    )
