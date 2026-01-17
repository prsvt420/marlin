"""Module required by Django to register administration configurations."""

from .translations import CityTranslationOptions  # noqa: F401 isort: skip
from .translations import (  # noqa: F401 isort: skip
    ProfessionalAreaTranslationOptions,
)
from .translations import RegionTranslationOptions  # noqa: F401 isort: skip
from .translations import VacancyTranslationOptions  # noqa: F401 isort: skip
from .admins import CityAdmin  # noqa: F401 isort: skip
from .admins import ProfessionalAreaAdmin  # noqa: F401 isort: skip
from .admins import RegionAdmin  # noqa: F401 isort: skip
from .admins import VacancyAdmin  # noqa: F401 isort: skip
