from django.db.models import QuerySet

from apps.catalog.models import ProductImage


class ProductImageSelector:

    def get_product_images(self) -> QuerySet[ProductImage]:
        return ProductImage.objects.all()
