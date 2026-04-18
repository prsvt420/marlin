from typing import Any, Dict

from django.http import HttpRequest

from apps.favorites.selectors import FavoriteSelector


def favorite(request: HttpRequest) -> Dict[str, Any]:
    if not request.user.is_authenticated:
        return {"favorite_product_pks": set()}

    favorite_product_pks: (
        set
    ) = FavoriteSelector().get_user_favorite_product_pks(
        user=request.user  # type: ignore
    )

    return {"favorite_product_pks": favorite_product_pks}
