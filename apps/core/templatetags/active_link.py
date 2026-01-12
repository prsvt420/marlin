from typing import Optional

from django import template
from django.core.handlers.wsgi import WSGIRequest
from django.urls import ResolverMatch, resolve

register: template.Library = template.Library()


@register.simple_tag
def active_link(request: WSGIRequest, url_name: str, class_name: str) -> str:
    """Returns a CSS class if the current URL matches the given route name."""
    resolver_match: ResolverMatch = resolve(request.path)
    current_url_name: Optional[str] = (
        f"{resolver_match.namespace}:{resolver_match.url_name}"
        if resolver_match.namespace
        else resolver_match.url_name
    )
    return class_name if current_url_name == url_name else ""
