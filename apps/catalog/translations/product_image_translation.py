from modeltranslation import translator

from apps.catalog.models import (
    ProductImage,
)


@translator.register(ProductImage)
class ProductImageTranslationOptions(translator.TranslationOptions):

    fields = ("alt_text",)
    required_languages = ("ru", "en")
