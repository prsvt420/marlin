from typing import Optional

from django import template
from django.core.handlers.wsgi import WSGIRequest
from django.urls import ResolverMatch, resolve

register: template.Library = template.Library()


@register.simple_tag
def active_link(request: WSGIRequest, url_name: str, class_name: str) -> str:
    """Determines whether a link is active and returns its CSS class.

    Compares the current URL template from the request with
    the specified URL template name.

    Args:
        request (WSGIRequest): Django HTTP Request Object.
        url_name (str): URL pattern name to compare against.
        class_name (str): CSS class to return when pattern names match.

    Returns:
        str: CSS class if the current URL template matches url_name,
        otherwise an empty string.
    """
    resolver_match: ResolverMatch = resolve(request.path)
    current_url_name: Optional[str] = (
        f"{resolver_match.namespace}:{resolver_match.url_name}"
        if resolver_match.namespace
        else resolver_match.url_name
    )
    return class_name if current_url_name == url_name else ""
