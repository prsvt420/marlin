from typing import Any, Union

from django.contrib.auth.mixins import AccessMixin
from django.http import HttpRequest, HttpResponse
from django_htmx.http import HttpResponseClientRedirect


class HtmxLoginRequiredMixin(AccessMixin):

    def dispatch(
        self, request: HttpRequest, **kwargs: Any
    ) -> Union[HttpResponse, HttpResponseClientRedirect]:
        if not request.user.is_authenticated:
            if request.htmx:  # type: ignore
                return HttpResponseClientRedirect(
                    redirect_to=self.get_login_url()
                )
            return self.handle_no_permission()
        return super().dispatch(request, **kwargs)  # type: ignore
