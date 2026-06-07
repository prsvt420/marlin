from django.db import transaction

from apps.accounts.models import User
from apps.reviews.exceptions import ProductReviewNotAllowedError
from apps.reviews.models import ProductReview
from apps.reviews.selectors import ProductReviewSelector


class ProductReviewService:

    @transaction.atomic
    def update_product_rating(
        self, *, user: User, product_pk: int, rating: int
    ) -> ProductReview:
        can_review_product: (
            bool
        ) = ProductReviewSelector().can_user_review_product(
            user=user,
            product_pk=product_pk,
        )

        if not can_review_product:
            raise ProductReviewNotAllowedError()

        product_review, _ = ProductReview.objects.update_or_create(
            user=user,
            product_id=product_pk,
            defaults={"rating": rating},
        )
        return product_review
