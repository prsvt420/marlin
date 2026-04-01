import django_filters
from django.contrib.postgres import search
from django.db.models import QuerySet

from apps.catalog.models import Product


class ProductSearchFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_search")

    class Meta:
        model = Product
        fields = ("q",)

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
