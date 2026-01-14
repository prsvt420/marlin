from modeltranslation import translator

from apps.catalog.models import (
    Attribute,
    Category,
    Product,
    ProductAttribute,
    ProductImage,
)


@translator.register(Product)
class ProductTranslationOptions(translator.TranslationOptions):
    """Configuration for translating the Product model."""

    fields = ("name", "description", "composition")
    required_languages = ("ru", "en")


@translator.register(Attribute)
class AttributeTranslationOptions(translator.TranslationOptions):
    """Configuration for translating the Attribute model."""

    fields = ("name",)
    required_languages = ("ru", "en")


@translator.register(ProductAttribute)
class ProductAttributeTranslationOptions(translator.TranslationOptions):
    """Configuration for translating the ProductAttribute model."""

    fields = ("value",)
    required_languages = ("ru", "en")


@translator.register(ProductImage)
class ProductImageTranslationOptions(translator.TranslationOptions):
    """Configuration for translating the ProductImage model."""

    fields = ("alt_text",)
    required_languages = ("ru", "en")


@translator.register(Category)
class CategoryTranslationOptions(translator.TranslationOptions):
    """Configuration for translating the Category model."""

    fields = ("name", "description", "alt_text")
    required_languages = ("ru", "en")
