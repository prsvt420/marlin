from modeltranslation import translator

from apps.vacancies.models import Vacancy


@translator.register(Vacancy)
class VacancyTranslationOptions(translator.TranslationOptions):
    """Configuration for translating the Vacancy model."""

    fields = ("title", "short_description", "description")
    required_languages = ("ru", "en")
