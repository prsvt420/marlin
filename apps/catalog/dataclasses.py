from dataclasses import dataclass
from typing import Optional

from django_stubs_ext import StrOrPromise


@dataclass(frozen=True)
class OrderingOption:
    """Data structure for a single ordering option."""

    field: Optional[str]
    label: StrOrPromise
