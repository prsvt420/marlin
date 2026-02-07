from modeltranslation import translator

from apps.vacancies.models import Vacancy


@translator.register(Vacancy)
class VacancyTranslationOptions(translator.TranslationOptions):

    fields = ("title", "short_description", "description")
    required_languages = ("ru", "en")
