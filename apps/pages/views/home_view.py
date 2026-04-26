from typing import Any, Dict

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from apps.catalog.selectors import ProductSelector


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"name": _("Home"), "url": reverse_lazy(viewname="pages:home")},
        ]
        context["popular_products"] = ProductSelector().get_popular_products()
        context["new_products"] = ProductSelector().get_new_products()

        return context
