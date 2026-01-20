from modeltranslation import translator

from apps.catalog.models import (
    ProductAttribute,
)


@translator.register(ProductAttribute)
class ProductAttributeTranslationOptions(translator.TranslationOptions):
    """Configuration for translating the ProductAttribute model."""

    fields = ("value",)
    required_languages = ("ru", "en")
