from modeltranslation import translator

from apps.catalog.models import (
    Attribute,
)


@translator.register(Attribute)
class AttributeTranslationOptions(translator.TranslationOptions):

    fields = ("name",)
    required_languages = ("ru", "en")
