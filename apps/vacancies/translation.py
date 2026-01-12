from modeltranslation import translator

from apps.vacancies.models import City, ProfessionalArea, Region, Vacancy


@translator.register(ProfessionalArea)
class ProfessionalAreaTranslationOptions(translator.TranslationOptions):
    """Configuration for translating the ProfessionalArea model."""

    fields = ("name",)
    required_languages = ("ru", "en")


@translator.register(Region)
class RegionTranslationOptions(translator.TranslationOptions):
    """Configuration for translating the Region model."""

    fields = ("name",)
    required_languages = ("ru", "en")


@translator.register(City)
class CityTranslationOptions(translator.TranslationOptions):
    """Configuration for translating the City model."""

    fields = ("name",)
    required_languages = ("ru", "en")


@translator.register(Vacancy)
class VacancyTranslationOptions(translator.TranslationOptions):
    """Configuration for translating the Vacancy model."""

    fields = ("title", "short_description", "description")
    required_languages = ("ru", "en")
