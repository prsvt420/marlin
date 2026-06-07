from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.catalog.selectors import ProductSelector
from apps.core.mixins import HtmxLoginRequiredMixin
from apps.reviews.exceptions import ProductReviewNotAllowedError
from apps.reviews.forms import ProductReviewForm
from apps.reviews.selectors import ProductReviewSelector
from apps.reviews.services import ProductReviewService


class ProductReviewUpdateView(HtmxLoginRequiredMixin, View):

    def post(self, request: HttpRequest, product_pk: int) -> HttpResponse:
        form = ProductReviewForm(data=request.POST)

        if not form.is_valid():
            messages.error(request, _("Select a rating from 1 to 5."))
        else:
            try:
                ProductReviewService().update_product_rating(
                    user=request.user,  # type: ignore
                    product_pk=product_pk,
                    rating=form.cleaned_data["rating"],
                )
            except ProductReviewNotAllowedError:
                messages.error(
                    request,
                    _("Only customers who ordered this product can rate it."),
                )
            except Exception:
                messages.error(
                    request,
                    _(
                        "An error occurred while saving the rating. "
                        "Please try again."
                    ),
                )

        if request.htmx:  # type: ignore
            product_review_selector = ProductReviewSelector()
            return render(
                request=request,
                template_name=(
                    "reviews/includes/_product_review_control_htmx.html"
                ),
                context={
                    "product": ProductSelector().get_product(
                        product_pk=product_pk,
                        only_active=False,
                    ),
                    "can_review_product": (
                        product_review_selector.can_user_review_product(
                            user=request.user,  # type: ignore
                            product_pk=product_pk,
                        )
                    ),
                    "product_review": (
                        product_review_selector.get_user_product_review(
                            user=request.user,  # type: ignore
                            product_pk=product_pk,
                        )
                    ),
                },
            )

        return redirect(to=request.META.get("HTTP_REFERER", "pages:home"))
