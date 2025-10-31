from typing import List

from django.urls import URLPattern, path

from . import views

app_name: str = "vacancies"

urlpatterns: List[URLPattern] = [
    path("", views.VacancyListView.as_view(), name="vacancy_list"),
]
