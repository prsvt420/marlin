from dataclasses import dataclass
from typing import Optional

from django_stubs_ext import StrOrPromise


@dataclass(frozen=True)
class OrderingOption:

    field: Optional[str]
    label: StrOrPromise
