from modeltranslation import translator

from apps.catalog.models import (
    Product,
)


@translator.register(Product)
class ProductTranslationOptions(translator.TranslationOptions):
    """Configuration for translating the Product model."""

    fields = ("name", "description", "composition")
    required_languages = ("ru", "en")
