from django.db.models import QuerySet

from apps.vacancies.models import City


class CitySelector:

    def get_cities(self) -> QuerySet[City]:
        return City.objects.select_related("region").all()
