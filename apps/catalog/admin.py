"""Module required by Django to register administration configurations."""

from apps.catalog.translations import (  # noqa: F401 isort: skip
    AttributeTranslationOptions,
)
from apps.catalog.translations import (  # noqa: F401 isort: skip
    CategoryTranslationOptions,
)
from apps.catalog.translations import (  # noqa: F401 isort: skip
    ProductAttributeTranslationOptions,
)
from apps.catalog.translations import (  # noqa: F401 isort: skip
    ProductImageTranslationOptions,
)
from apps.catalog.translations import (  # noqa: F401 isort: skip
    ProductTranslationOptions,
)
from apps.catalog.admins import (  # noqa: F401 isort: skip
    ProductAttributeInline,
)
from apps.catalog.admins import ProductImageInline  # noqa: F401 isort: skip
from apps.catalog.admins import (  # noqa: F401 isort: skip
    ProductNutritionInline,
)
from apps.catalog.admins import Attribute  # noqa: F401 isort: skip
from apps.catalog.admins import Category  # noqa: F401 isort: skip
from apps.catalog.admins import Product  # noqa: F401 isort: skip
from apps.catalog.admins import ProductAttribute  # noqa: F401 isort: skip
from apps.catalog.admins import ProductImage  # noqa: F401 isort: skip
from apps.catalog.admins import ProductNutrition  # noqa: F401 isort: skip
