from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class PrivacyView(TemplateView):
    template_name = "pages/redesign/privacy.html"
    extra_context = {
        "breadcrumbs": [
            {"name": _("Home"), "url": reverse_lazy(viewname="pages:home")},
            {
                "name": _("Privacy Policy"),
                "url": reverse_lazy(viewname="pages:privacy"),
            },
        ]
    }
