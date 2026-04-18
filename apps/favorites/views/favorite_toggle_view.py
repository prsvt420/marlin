from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.core.mixins import HtmxLoginRequiredMixin
from apps.favorites.services import FavoriteService


class FavoriteToggleView(HtmxLoginRequiredMixin, View):

    def post(self, request: HttpRequest, product_pk: int) -> HttpResponse:
        try:
            was_toggled: bool = FavoriteService().toggle_favorite(
                user=request.user,  # type: ignore
                product_pk=product_pk,
            )
        except Exception:
            messages.error(
                request,
                _(
                    "An error occurred while adding the product to favorites. "
                    "Please try again."
                ),
            )
        else:
            if was_toggled:
                messages.success(
                    request,
                    _("The product has been successfully added to favorites."),
                )
            else:
                messages.success(
                    request,
                    _(
                        "The product has been successfully removed "
                        "from favorites."
                    ),
                )

        if request.htmx:  # type: ignore
            return render(
                request=request,
                template_name="favorites/includes/_favorite_button_htmx.html",
                context={"product_pk": product_pk},
            )

        return redirect(to=request.META.get("HTTP_REFERER", "pages:home"))
