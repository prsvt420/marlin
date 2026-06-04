from typing import Any, Dict, List, Optional

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from apps.accounts.forms.profile_form import ProfileForm
from apps.accounts.models import User
from apps.orders.models import Order
from apps.orders.selectors import OrderSelector


class ProfileView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = "accounts/profile.html"
    success_message = _(
        "Your profile information has been successfully updated."
    )
    success_url = reverse_lazy(viewname="accounts:profile")
    form_class = ProfileForm

    def get_object(self, queryset: Optional[QuerySet[User]] = None) -> User:
        return self.request.user  # type: ignore

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        social_accounts = list(
            self.object.social_auth.order_by("-modified")
        )  # type: ignore
        recent_orders: List[Order] = list(
            OrderSelector().get_user_recent_orders(user=self.object)
        )

        context["breadcrumbs"] = [
            {"name": _("Home"), "url": reverse_lazy(viewname="pages:home")},
            {
                "name": _("Profile"),
                "url": reverse_lazy(viewname="accounts:profile"),
            },
        ]
        context["recent_orders"] = recent_orders
        context["social_accounts"] = social_accounts
        context["connected_social_providers"] = {
            social_account.provider for social_account in social_accounts
        }
        return context

    def form_invalid(self, form: ProfileForm) -> HttpResponse:
        messages.error(
            self.request,
            _("Please correct the errors in the form and try again."),
        )
        return super().form_invalid(form=form)
