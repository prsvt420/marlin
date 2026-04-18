from typing import Set

from django.db.models import Prefetch, QuerySet

from apps.accounts.models import User
from apps.catalog.selectors import ProductSelector
from apps.favorites.models import Favorite


class FavoriteSelector:

    def get_user_favorites(self, *, user: User) -> QuerySet[Favorite]:
        return Favorite.objects.filter(user=user).prefetch_related(
            Prefetch(
                lookup="product",
                queryset=ProductSelector().get_products(only_active=False),
            )
        )

    def get_user_favorite_product_pks(self, *, user: User) -> Set[int]:
        return set(
            Favorite.objects.filter(user=user).values_list(
                "product_id", flat=True
            )
        )
