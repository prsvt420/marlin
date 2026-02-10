from smtplib import SMTPException
from typing import Any, List, Mapping, Optional

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from apps.core.dataclasses import EmailTemplate
from apps.core.exceptions import EmailSendError
from config import settings


class EmailService:
    def send_email(
        self,
        *,
        from_email: str = settings.DEFAULT_FROM_EMAIL,
        email_template: EmailTemplate,
        to: List[str],
        context: Optional[Mapping[str, Any]] = None,
    ) -> None:
        try:
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
                from_email=from_email,
                to=to,
            )
            email_message.attach_alternative(
                content=content, mimetype="text/html"
            )
            email_message.send()
        except (SMTPException, OSError) as error:
            raise EmailSendError("Couldn't send a email") from error
