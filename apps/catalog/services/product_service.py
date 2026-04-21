from decimal import Decimal

from django.db.models import F

from apps.catalog.models import Product


class ProductService:
    def decrease_stock(self, *, product_pk: int, quantity: Decimal) -> None:
        Product.objects.filter(pk=product_pk).update(
            stock=F("stock") - quantity
        )
