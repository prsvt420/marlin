from typing import List

from django.urls import URLPattern, path

from apps.vacancies import views

app_name: str = "vacancies"

urlpatterns: List[URLPattern] = [
    path(route="", view=views.VacancyListView.as_view(), name="list"),
    path(
        route="<int:vacancy_pk>/",
        view=views.VacancyDetailView.as_view(),
        name="detail",
    ),
]
