from dataclasses import dataclass
from typing import Optional

from django_stubs_ext import StrOrPromise


@dataclass(frozen=True)
class OrderingOption:
    """Represents a single product ordering option.

    Attributes:
        field (Optional[str]): The model field or annotated expression
            used for ordering in a QuerySet.
        label (StrOrPromise): A human-readable label for this ordering option.
    """

    field: Optional[str]
    label: StrOrPromise
