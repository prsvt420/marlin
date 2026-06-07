from typing import Optional

from apps.accounts.models import User
from apps.orders.models import OrderItem
from apps.reviews.models import ProductReview


class ProductReviewSelector:

    def can_user_review_product(self, *, user: User, product_pk: int) -> bool:
        return OrderItem.objects.filter(
            order__user=user,
            product_id=product_pk,
        ).exists()

    def get_user_product_review(
        self, *, user: User, product_pk: int
    ) -> Optional[ProductReview]:
        return ProductReview.objects.filter(
            user=user,
            product_id=product_pk,
        ).first()
