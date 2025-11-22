from dataclasses import dataclass
from typing import Optional

from django.utils.functional import Promise


@dataclass(frozen=True)
class OrderingOption:
    """Represents a single product ordering option.

    Attributes:
        field (Optional[str]): The model field or annotated expression
            used for ordering in a QuerySet.
        label (Promise): A human-readable label for this ordering option.
    """

    field: Optional[str]
    label: Promise
