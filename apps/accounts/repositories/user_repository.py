from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.shortcuts import get_object_or_404

User: type[AbstractBaseUser] = get_user_model()


class UserRepository:
    """Repository for Category model database operations."""

    @staticmethod
    def get_by_pk(pk: str) -> AbstractBaseUser:
        """Return a user by its pk.

        Args:
            pk (str): The pk of the user to retrieve.

        Returns:
            AbstractBaseUser: The User object matching the given pk.

        Raises:
            Http404: If no user with the given pk is found.
        """
        return get_object_or_404(User, pk=pk)

    @staticmethod
    def activate(user: AbstractBaseUser) -> None:
        """Activate the given user.

        Args:
            user (AbstractBaseUser): The user to activate.
        """
        user.is_active = True
        user.save(update_fields=["is_active"])
