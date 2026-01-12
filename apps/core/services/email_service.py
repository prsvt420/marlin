from typing import Any, List, Mapping, Optional

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from apps.core.dataclasses import EmailTemplate
from config import settings


class EmailService:
    """Service for sending emails."""

    def __init__(  # noqa: D107
        self, from_email: str = settings.DEFAULT_FROM_EMAIL
    ) -> None:
        self._from_email: str = from_email

    def send_email(
        self,
        *,
        email_template: EmailTemplate,
        to: List[str],
        context: Optional[Mapping[str, Any]] = None,
    ) -> None:
        """Send an email rendered from the specified email template."""
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
