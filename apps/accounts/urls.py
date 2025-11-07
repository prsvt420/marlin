from typing import List

from django.urls import URLPattern, path

from . import views

app_name: str = "accounts"

urlpatterns: List[URLPattern] = [
    path("signin", views.SignInView.as_view(), name="signin"),
    path("signout", views.SignOutView.as_view(), name="signout"),
    path("signup", views.SignUpView.as_view(), name="signup"),
]
