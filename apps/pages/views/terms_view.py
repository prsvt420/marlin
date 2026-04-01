from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class TermsView(TemplateView):
    template_name = "pages/redesign/terms.html"
    extra_context = {
        "breadcrumbs": [
            {"name": _("Home"), "url": reverse_lazy(viewname="pages:home")},
            {
                "name": _("Terms of Service"),
                "url": reverse_lazy(viewname="pages:terms"),
            },
        ]
    }
