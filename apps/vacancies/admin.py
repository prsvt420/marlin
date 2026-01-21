"""Module required by Django to register administration configurations."""

from apps.vacancies.translations import (  # noqa: F401 isort: skip
    CityTranslationOptions,
)
from apps.vacancies.translations import (  # noqa: F401 isort: skip
    ProfessionalAreaTranslationOptions,
)
from apps.vacancies.translations import (  # noqa: F401 isort: skip
    RegionTranslationOptions,
)
from apps.vacancies.translations import (  # noqa: F401 isort: skip
    VacancyTranslationOptions,
)
from apps.vacancies.admins import CityAdmin  # noqa: F401 isort: skip
from apps.vacancies.admins import (  # noqa: F401 isort: skip
    ProfessionalAreaAdmin,
)
from apps.vacancies.admins import RegionAdmin  # noqa: F401 isort: skip
from apps.vacancies.admins import VacancyAdmin  # noqa: F401 isort: skip
