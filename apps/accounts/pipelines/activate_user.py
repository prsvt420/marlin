from typing import Any

from apps.accounts.models import User


def activate_user(user: User, **kwargs: Any) -> None:
    if user and not user.is_active:
        user.is_active = True
        user.save(update_fields=["is_active"])
