from typing import List

from django.urls import URLPattern, path

from apps.accounts import views

app_name: str = "accounts"

urlpatterns: List[URLPattern] = [
    path("signin", views.SignInView.as_view(), name="signin"),
    path("signout", views.SignOutView.as_view(), name="signout"),
    path("signup", views.SignUpView.as_view(), name="signup"),
    path(
        "password-reset",
        views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset/<uidb64>/<token>",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "account-activation/<uidb64>/<token>",
        views.AccountActivationView.as_view(),
        name="account_activation",
    ),
]
