from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView


class SignInView(SuccessMessageMixin, LoginView):
    """Displays the sign in page.

    Renders the `accounts/signin.html` template with a AuthenticationForm.
    """

    template_name = "accounts/signin.html"
    success_message = _("You have successfully signed in. Welcome!")
    redirect_authenticated_user = True

    def form_invalid(self, form: AuthenticationForm) -> HttpResponse:
        """Handle invalid form submission.

        Displays an error message to the user when the sign in form
        contains validation errors. The message in forms the user to
        correct the errors and try again.

        Args:
            form (AuthenticationForm): The invalid sign in form
            instance with validation errors.

        Returns:
            HttpResponse: The HTTP response returned by the parent class's
            form_invalid method, which re-renders the form with error messages.
        """
        messages.error(
            self.request,
            _("Please correct the errors in the form and try again."),
        )
        return super().form_invalid(form)


class SignOutView(LogoutView):
    """Handles user sign out functionality.

    Extends Django's LogoutView to provide custom success message
    feedback to users upon successful logout.
    """

    def get_redirect_url(self) -> str:
        """Process logout redirect with success message.

        Displays a success message confirming the logout operation
        before redirecting the user to the appropriate URL.

        Returns:
            str: The redirect URL returned by the parent class's
            get_redirect_url method, typically the homepage or
            login page.
        """
        messages.success(
            self.request, _("You have been signed out. Have a nice day!")
        )
        return super().get_redirect_url()


class SignUpView(SuccessMessageMixin, CreateView):
    """Displays the sign up page.

    Renders the `accounts/signup.html` template with a UserCreationForm.
    """

    template_name = "accounts/signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("accounts:signin")
    success_message = _(
        "You have successfully signed up! Sign in to your account."
    )

    def form_invalid(self, form: UserCreationForm) -> HttpResponse:
        """Handle invalid form submission.

        Displays an error message to the user when the sign up form
        contains validation errors. The message in forms the user to
        correct the errors and try again.

        Args:
            form (UserCreationForm): The invalid sign up form
            instance with validation errors.

        Returns:
            HttpResponse: The HTTP response returned by the parent class's
            form_invalid method, which re-renders the form with error messages.
        """
        messages.error(
            self.request,
            _("Please correct the errors in the form and try again."),
        )
        return super().form_invalid(form)
