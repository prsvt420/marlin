from typing import Any, Dict, Optional

from django import template

register: template.Library = template.Library()


@register.filter
def get_item(dictionary: Dict[Any, Any], key: Any) -> Optional[Any]:
    return dictionary.get(key)
