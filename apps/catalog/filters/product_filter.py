import django_filters
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from apps.catalog.models import Product


class ProductFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_search")
    sort = django_filters.OrderingFilter(
        fields=(
            ("final_price", "price"),
            ("discount", "discount"),
        ),
        field_labels={
            "price": _("Price"),
            "discount": _("Discount"),
            "-price": _("Price (descending)"),
            "-discount": _("Discount (descending)"),
        },
        empty_label=_("Default"),
        label=_("Sorting"),
    )

    class Meta:
        model = Product
        fields = ("q", "sort")

    def filter_search(
        self, queryset: QuerySet[Product], name: str, value: str
    ) -> QuerySet[Product]:
        if not value:
            return queryset

        return queryset.filter(name__icontains=value)
