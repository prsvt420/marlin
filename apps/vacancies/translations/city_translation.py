from modeltranslation import translator

from apps.vacancies.models import City


@translator.register(City)
class CityTranslationOptions(translator.TranslationOptions):
    fields = ("name",)
    required_languages = ("ru", "en")
