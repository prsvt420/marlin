from modeltranslation import translator

from apps.catalog.models import (
    Category,
)


@translator.register(Category)
class CategoryTranslationOptions(translator.TranslationOptions):
    """Configuration for translating the Category model."""

    fields = ("name", "description", "alt_text")
    required_languages = ("ru", "en")
