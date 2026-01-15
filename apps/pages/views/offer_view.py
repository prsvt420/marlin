from django.views.generic import TemplateView


class OfferView(TemplateView):
    """View for displaying the public offer."""

    template_name = "pages/offer.html"
