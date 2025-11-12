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
    """Translation options for Product model."""

    fields = ("name", "description", "composition")
    required_languages = ("ru", "en")


@translator.register(Attribute)
class AttributeTranslationOptions(translator.TranslationOptions):
    """Translation options for Attribute model."""

    fields = ("name",)
    required_languages = ("ru", "en")


@translator.register(ProductAttribute)
class ProductAttributeTranslationOptions(translator.TranslationOptions):
    """Translation options for ProductAttribute model."""

    fields = ("value",)
    required_languages = ("ru", "en")


@translator.register(ProductImage)
class ProductImageTranslationOptions(translator.TranslationOptions):
    """Translation options for ProductImage model."""

    fields = ("alt_text",)
    required_languages = ("ru", "en")


@translator.register(Category)
class CategoryTranslationOptions(translator.TranslationOptions):
    """Translation options for Category model."""

    fields = ("name", "description")
    required_languages = ("ru", "en")
