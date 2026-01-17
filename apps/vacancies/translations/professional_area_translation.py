from modeltranslation import translator

from apps.vacancies.models import ProfessionalArea


@translator.register(ProfessionalArea)
class ProfessionalAreaTranslationOptions(translator.TranslationOptions):
    """Configuration for translating the ProfessionalArea model."""

    fields = ("name",)
    required_languages = ("ru", "en")
