from typing import List, Union

from django.urls import URLPattern, URLResolver, include, path
from django_ratelimit.decorators import ratelimit

from apps.accounts import views

app_name: str = "accounts"

urlpatterns: List[Union[URLResolver, URLPattern]] = [
    path(
        route="",
        view=include(arg="social_django.urls", namespace="social"),
        name="social",
    ),
    path(
        route="signin/",
        view=ratelimit(key="ip", method="post", rate="5/m", block=True)(
            views.SignInView.as_view()
        ),
        name="signin",
    ),
    path(route="signout/", view=views.SignOutView.as_view(), name="signout"),
    path(
        route="signup/",
        view=ratelimit(key="ip", method="post", rate="10/m", block=True)(
            views.SignUpView.as_view()
        ),
        name="signup",
    ),
    path(
        route="password-reset/",
        view=ratelimit(key="ip", method="post", rate="3/m", block=True)(
            views.PasswordResetView.as_view()
        ),
        name="password-reset",
    ),
    path(
        route="password-reset/<uidb64>/<token>/",
        view=ratelimit(key="ip", rate="5/m", block=True)(
            views.PasswordResetConfirmView.as_view()
        ),
        name="password-reset-confirm",
    ),
    path(
        route="activate/<uidb64>/<token>/",
        view=ratelimit(key="ip", rate="5/m", block=True)(
            views.AccountActivateView.as_view()
        ),
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
