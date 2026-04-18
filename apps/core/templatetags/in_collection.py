from typing import Any, Iterable

from django import template

register = template.Library()


@register.filter
def in_collection(value: Any, collection: Iterable[Any]) -> bool:
    return value in collection
