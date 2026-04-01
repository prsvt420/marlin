from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class OfferView(TemplateView):
    template_name = "pages/redesign/offer.html"
    extra_context = {
        "breadcrumbs": [
            {"name": _("Home"), "url": reverse_lazy(viewname="pages:home")},
            {
                "name": _("Public Offer"),
                "url": reverse_lazy(viewname="pages:offer"),
            },
        ]
    }
