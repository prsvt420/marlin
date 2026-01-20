"""Module required by Django to register administration configurations."""

from .translations import AttributeTranslationOptions  # noqa: F401 isort: skip
from .translations import CategoryTranslationOptions  # noqa: F401 isort: skip
from .translations import (  # noqa: F401 isort: skip
    ProductAttributeTranslationOptions,
)
from .translations import (  # noqa: F401 isort: skip
    ProductImageTranslationOptions,
)
from .translations import ProductTranslationOptions  # noqa: F401 isort: skip
from .admins import ProductAttributeInline  # noqa: F401 isort: skip
from .admins import ProductImageInline  # noqa: F401 isort: skip
from .admins import ProductNutritionInline  # noqa: F401 isort: skip
from .admins import Attribute  # noqa: F401 isort: skip
from .admins import Category  # noqa: F401 isort: skip
from .admins import Product  # noqa: F401 isort: skip
from .admins import ProductAttribute  # noqa: F401 isort: skip
from .admins import ProductImage  # noqa: F401 isort: skip
from .admins import ProductNutrition  # noqa: F401 isort: skip
