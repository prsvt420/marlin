from django.views.generic import TemplateView


class PrivacyView(TemplateView):
    """View for displaying the privacy policy."""

    template_name = "pages/privacy.html"
