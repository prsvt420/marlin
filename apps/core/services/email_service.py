from typing import Any, List, Mapping

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from apps.core.dataclasses import EmailTemplate
from config import settings


class EmailService:
    """Service for sending emails."""

    def __init__(self, from_email: str = settings.DEFAULT_FROM_EMAIL) -> None:
        """Initialize the email service with a sender email.

        Args:
            from_email (str): Email address to use as sender.
                Defaults to settings.DEFAULT_FROM_EMAIL if not provided.
        """
        self._from_email: str = from_email

    def send_email(
        self,
        *,
        email_template: EmailTemplate,
        to: List[str],
        context: Mapping[str, Any],
    ) -> None:
        """Send an email with HTML content rendered from a template.

        Args:
            email_template (EmailTemplate): Email template containing
            paths for subject, plain text body, and HTML content.
            to (List[str]): List of recipient email addresses.
            context (Mapping[str, Any]): Context data for rendering the
            templates.
        """
        subject: str = render_to_string(
            template_name=email_template.subject, context=context
        ).strip()
        body: str = render_to_string(
            template_name=email_template.body, context=context
        )
        content: str = render_to_string(
            template_name=email_template.content, context=context
        )
        email_message: EmailMultiAlternatives = EmailMultiAlternatives(
            subject=subject,
            body=body,
            from_email=self._from_email,
            to=to,
        )

        email_message.attach_alternative(content=content, mimetype="text/html")
        email_message.send()
