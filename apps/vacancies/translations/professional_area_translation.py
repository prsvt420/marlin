from modeltranslation import translator

from apps.vacancies.models import ProfessionalArea


@translator.register(ProfessionalArea)
class ProfessionalAreaTranslationOptions(translator.TranslationOptions):

    fields = ("name",)
    required_languages = ("ru", "en")
