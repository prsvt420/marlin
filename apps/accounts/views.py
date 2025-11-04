from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse


class SignInView(SuccessMessageMixin, LoginView):
    """Displays the sign in page.

    Renders the 'pages/contact.html' template with a SignInForm.
    """

    template_name = "accounts/signin.html"
    success_message = "Вы успешно авторизованы. Добро пожаловать!"
    redirect_authenticated_user = True

    def form_invalid(self, form: AuthenticationForm) -> HttpResponse:
        """Handle invalid form submission.

        Displays an error message to the user when the sign in form
        contains validation errors. The message informs the user to
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
            "Пожалуйста, исправьте ошибки в форме и попробуйте снова.",
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
        messages.success(self.request, "Вы вышли из аккаунта. Хорошего дня!")
        return super().get_redirect_url()
