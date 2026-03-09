import django_filters
from django.contrib.postgres import search
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

        search_vector: search.SearchVector = search.SearchVector("name")
        search_query: search.SearchQuery = search.SearchQuery(value=value)

        return (
            queryset.annotate(
                search=search_vector,
                rank=search.SearchRank(
                    search_vector, search_query, cover_density=True
                ),
            )
            .filter(search=search_query)
            .order_by("-rank")
        )
