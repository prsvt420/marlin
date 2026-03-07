from modeltranslation import translator

from apps.catalog.models import (
    Category,
)


@translator.register(Category)
class CategoryTranslationOptions(translator.TranslationOptions):
    fields = ("name", "description")
    required_languages = ("ru", "en")
