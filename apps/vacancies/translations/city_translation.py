from modeltranslation import translator

from apps.vacancies.models import City


@translator.register(City)
class CityTranslationOptions(translator.TranslationOptions):
    """Configuration for translating the City model."""

    fields = ("name",)
    required_languages = ("ru", "en")
