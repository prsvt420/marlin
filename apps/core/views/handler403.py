from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django_ratelimit.exceptions import Ratelimited


def handler403(request: HttpRequest, exception=None) -> HttpResponse:
    if isinstance(exception, Ratelimited):
        return render(request=request, template_name="429.html", status=429)
    return render(request=request, template_name="403.html", status=403)
