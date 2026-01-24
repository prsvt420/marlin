from typing import Optional

from django.contrib import messages
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from apps.accounts.forms.profile_form import ProfileForm


class ProfileView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """View for handling the profile form."""

    template_name = "accounts/profile.html"
    success_message = _(
        "Your profile information has been successfully updated."
    )
    success_url = reverse_lazy("accounts:profile")
    form_class = ProfileForm

    def get_object(
        self, queryset: Optional[QuerySet] = None
    ) -> AbstractBaseUser:
        """Return current user."""
        return self.request.user  # type: ignore

    def form_invalid(self, form: ProfileForm) -> HttpResponse:
        """Handle an invalid profile form and display an error message."""
        messages.error(
            self.request,
            _("Please correct the errors in the form and try again."),
        )
        return super().form_invalid(form)
