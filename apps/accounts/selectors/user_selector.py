from typing import Optional

from apps.accounts.models import User


class UserSelector:

    def get_user(self, *, user_pk: int) -> Optional[User]:
        return User.objects.filter(pk=user_pk).first()

    def get_user_by_email(self, *, email: str) -> Optional[User]:
        return User.objects.filter(email=email).first()
