from django.db.models import QuerySet

from apps.catalog.models import ProductAttribute


class ProductAttributeSelector:
    def get_product_attributes(self) -> QuerySet[ProductAttribute]:
        return ProductAttribute.objects.select_related("attribute")
