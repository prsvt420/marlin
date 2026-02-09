from typing import Optional

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView


class AccountDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    """View for deleting the user account."""

    success_message = _(
        "Your account has been successfully deleted. Have a nice day!"
    )
    success_url = reverse_lazy("catalog:category-list")

    def get_object(
        self, queryset: Optional[QuerySet] = None
    ) -> AbstractBaseUser:
        """Return current user."""
        return self.request.user  # type: ignore
