from django.contrib import messages
from django.contrib.auth.views import (
    LogoutView,
)
from django.utils.translation import gettext_lazy as _


class SignOutView(LogoutView):
    """View for handling the sign out."""

    def get_redirect_url(self) -> str:
        """Add a success message and return the logout redirect URL."""
        messages.success(
            self.request, _("You have been signed out. Have a nice day!")
        )
        return super().get_redirect_url()
