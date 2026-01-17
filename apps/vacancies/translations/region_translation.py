from modeltranslation import translator

from apps.vacancies.models import Region


@translator.register(Region)
class RegionTranslationOptions(translator.TranslationOptions):
    """Configuration for translating the Region model."""

    fields = ("name",)
    required_languages = ("ru", "en")
