from modeltranslation import translator

from apps.catalog.models import (
    Product,
)


@translator.register(Product)
class ProductTranslationOptions(translator.TranslationOptions):
    fields = ("name", "description", "composition")
    required_languages = ("ru", "en")
