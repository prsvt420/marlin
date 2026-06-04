from typing import Any, Dict, Optional

from django.contrib import messages
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from social_core.storage import UserProtocol

from apps.accounts.models import User
from apps.accounts.selectors import UserSelector
from apps.accounts.services import UserService


def associate_by_email(
    details: Dict[str, Any],
    request: HttpRequest,
    user: Optional[UserProtocol] = None,
    **kwargs: Any,
) -> Optional[Dict[str, Any]]:
    if user:
        return None

    email: Optional[str] = details.get("email")

    if not email:
        return None

    existing_user: Optional[User] = UserSelector().get_user_by_email(
        email=email
    )

    if not existing_user:
        return None

    if not existing_user.is_active:
        UserService().reset_password_to_unusable(user=existing_user)
        messages.info(
            request,
            _(
                "Your account was linked to Google. "
                "Old password has been reset."
            ),
        )

    return {"user": existing_user, "is_new": False}
