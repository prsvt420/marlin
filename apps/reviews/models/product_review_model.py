from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.catalog.models import Product
from apps.core.models import BaseModel


class ProductReview(BaseModel):  # type: ignore
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("user"),
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("product"),
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=5),
        ],
        verbose_name=_("rating"),
    )

    class Meta:
        db_table = "reviews_product_review"
        db_table_comment = "Table containing product reviews."
        verbose_name = _("product review")
        verbose_name_plural = _("product reviews")
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_product_review_user_product",
                violation_error_message=_(
                    "You have already reviewed this product."
                ),
            ),
            models.CheckConstraint(
                condition=models.Q(rating__gte=1, rating__lte=5),
                name="check_product_review_rating_range",
                violation_error_message=_("Rating must be between 1 and 5."),
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user}: {self.product} — {self.rating}"
