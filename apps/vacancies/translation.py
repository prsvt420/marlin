from modeltranslation import translator

from apps.vacancies.models import City, ProfessionalArea, Region, Vacancy


@translator.register(ProfessionalArea)
class ProfessionalAreaTranslationOptions(translator.TranslationOptions):
    """Translation options for ProfessionalArea model."""

    fields = ("name",)
    required_languages = ("ru", "en")


@translator.register(Region)
class RegionTranslationOptions(translator.TranslationOptions):
    """Translation options for Region model."""

    fields = ("name",)
    required_languages = ("ru", "en")


@translator.register(City)
class CityTranslationOptions(translator.TranslationOptions):
    """Translation options for City model."""

    fields = ("name",)
    required_languages = ("ru", "en")


@translator.register(Vacancy)
class VacancyTranslationOptions(translator.TranslationOptions):
    """Translation options for Vacancy model."""

    fields = ("title", "short_description", "description")
    required_languages = ("ru", "en")
