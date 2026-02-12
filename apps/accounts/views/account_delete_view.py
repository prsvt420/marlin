from typing import Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DeleteView

from apps.accounts.models import User


class AccountDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    success_message = _(
        "Your account has been successfully deleted. Have a nice day!"
    )
    success_url = reverse_lazy(viewname="pages:home")

    def get_object(self, queryset: Optional[QuerySet[User]] = None) -> User:
        return self.request.user  # type: ignore
