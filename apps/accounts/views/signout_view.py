from django.contrib import messages
from django.contrib.auth.views import (
    LogoutView,
)
from django.utils.translation import gettext_lazy as _


class SignOutView(LogoutView):
    def get_redirect_url(self) -> str:
        messages.success(
            self.request, _("You have been signed out. Have a nice day!")
        )
        return super().get_redirect_url()
