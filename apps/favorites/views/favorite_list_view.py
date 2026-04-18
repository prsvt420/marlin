from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView

from apps.core.mixins import HtmxLoginRequiredMixin
from apps.favorites.models import Favorite
from apps.favorites.selectors import FavoriteSelector


class FavoriteListView(HtmxLoginRequiredMixin, ListView):
    template_name = "favorites/favorite_list.html"
    context_object_name = "favorites"
    paginate_by = 20
    paginate_orphans = 4
    extra_context = {
        "breadcrumbs": [
            {"name": _("Home"), "url": reverse_lazy(viewname="pages:home")},
            {
                "name": _("Favorites"),
                "url": reverse_lazy(viewname="favorites:list"),
            },
        ]
    }

    def get_queryset(self) -> QuerySet[Favorite]:
        return FavoriteSelector().get_user_favorites(
            user=self.request.user  # type: ignore
        )
