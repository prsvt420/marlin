from django.views.generic import TemplateView


class TermsView(TemplateView):
    """View for displaying the terms and conditions."""

    template_name = "pages/terms.html"
