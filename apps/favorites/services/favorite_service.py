from django.db import transaction

from apps.accounts.models import User
from apps.favorites.models import Favorite


class FavoriteService:

    @transaction.atomic
    def toggle_favorite(self, *, user: User, product_pk: int) -> bool:
        deleted_count, _ = Favorite.objects.filter(
            user=user, product_id=product_pk
        ).delete()

        if deleted_count > 0:
            return False

        Favorite.objects.create(user=user, product_id=product_pk)
        return True
