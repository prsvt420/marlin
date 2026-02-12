from typing import List

from django.urls import URLPattern, path

from apps.accounts import views

app_name: str = "accounts"

urlpatterns: List[URLPattern] = [
    path(route="signin/", view=views.SignInView.as_view(), name="signin"),
    path(route="signout/", view=views.SignOutView.as_view(), name="signout"),
    path(route="signup/", view=views.SignUpView.as_view(), name="signup"),
    path(
        route="password-reset/",
        view=views.PasswordResetView.as_view(),
        name="password-reset",
    ),
    path(
        route="password-reset/<uidb64>/<token>/",
        view=views.PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        route="activate/<uidb64>/<token>/",
        view=views.AccountActivateView.as_view(),
        name="activate",
    ),
    path(
        route="delete/",
        view=views.AccountDeleteView.as_view(),
        name="delete",
    ),
    path(
        route="profile/",
        view=views.ProfileView.as_view(),
        name="profile",
    ),
]
