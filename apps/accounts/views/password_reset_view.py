from django.contrib.auth.views import PasswordResetView as _PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from apps.accounts.forms import PasswordResetForm


class PasswordResetView(SuccessMessageMixin, _PasswordResetView):
    """View for handling the password reset form."""

    template_name = "accounts/password_reset.html"
    email_template_name = "emails/password_reset.txt"
    subject_template_name = "emails/password_reset_subject.txt"
    html_email_template_name = "emails/password_reset.html"
    success_message = _("A password reset link has been sent to your email.")
    success_url = reverse_lazy("accounts:signin")
    form_class = PasswordResetForm
