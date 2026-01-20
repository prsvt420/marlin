from modeltranslation import translator

from apps.catalog.models import (
    Attribute,
)


@translator.register(Attribute)
class AttributeTranslationOptions(translator.TranslationOptions):
    """Configuration for translating the Attribute model."""

    fields = ("name",)
    required_languages = ("ru", "en")
