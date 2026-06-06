from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext_lazy as _
from django.views import View


class VkAuthUnavailableView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        messages.error(
            request,
            _(
                "VK ID authorization is temporarily unavailable. "
                "Please try another method."
            ),
        )

        redirect_to: str = request.GET.get("next", "")
        if redirect_to and url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(to=redirect_to)

        return redirect(to="accounts:signin")
