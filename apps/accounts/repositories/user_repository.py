from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.shortcuts import get_object_or_404

User: type[AbstractBaseUser] = get_user_model()


class UserRepository:
    """Repository for accessing User model."""

    @staticmethod
    def get_by_pk(pk: str) -> AbstractBaseUser:
        """Retrieve a user by primary key or raise 404 if not found."""
        return get_object_or_404(User, pk=pk)

    @staticmethod
    def activate_user(user: AbstractBaseUser) -> None:
        """Activate the given user account."""
        user.is_active = True
        user.save(update_fields=["is_active"])
