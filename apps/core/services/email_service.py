from typing import Any, List, Mapping, Optional, Tuple

from django.template.loader import render_to_string

from apps.core.dataclasses import EmailTemplate
from apps.core.tasks import send_email_task
from config import settings


class EmailService:

    def _render_email_parts(
        self,
        *,
        email_template: EmailTemplate,
        context: Optional[Mapping[str, Any]],
    ) -> Tuple[str, ...]:
        subject: str = render_to_string(
            template_name=email_template.subject, context=context
        ).strip()
        body: str = render_to_string(
            template_name=email_template.body, context=context
        )
        content: str = render_to_string(
            template_name=email_template.content, context=context
        )

        return subject, body, content

    def send_email(
        self,
        *,
        from_email: str = settings.DEFAULT_FROM_EMAIL,
        email_template: EmailTemplate,
        to: List[str],
        context: Optional[Mapping[str, Any]] = None,
    ) -> None:

        subject, body, content = self._render_email_parts(
            email_template=email_template, context=context
        )

        send_email_task.delay(
            subject=subject,
            body=body,
            content=content,
            from_email=from_email,
            to=to,
        )
