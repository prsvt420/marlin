from django.db.models import QuerySet

from apps.vacancies.models import ProfessionalArea


class ProfessionalAreaSelector:

    def get_professional_areas(self) -> QuerySet[ProfessionalArea]:
        return ProfessionalArea.objects.all()
