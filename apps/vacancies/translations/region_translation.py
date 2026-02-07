from modeltranslation import translator

from apps.vacancies.models import Region


@translator.register(Region)
class RegionTranslationOptions(translator.TranslationOptions):

    fields = ("name",)
    required_languages = ("ru", "en")
