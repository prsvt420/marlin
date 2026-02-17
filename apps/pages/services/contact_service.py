from typing import Any, Mapping

from apps.core.services import EmailService
from apps.pages.email_templates import (
    CONTACT_INBOUND_EMAIL,
    CONTACT_OUTBOUND_EMAIL,
)
from config import settings


class ContactService:

    def __init__(self) -> None:
        self._email_service: EmailService = EmailService()

    def send_contact_emails(self, *, context: Mapping[str, Any]) -> None:
        self._send_contact_inbound_email(context=context)
        self._send_contact_outbound_email(context=context)

    def _send_contact_inbound_email(
        self, *, context: Mapping[str, Any]
    ) -> None:
        self._email_service.send_email(
            email_template=CONTACT_INBOUND_EMAIL,
            to=[settings.DEFAULT_FROM_EMAIL],
            context=context,
        )

    def _send_contact_outbound_email(
        self, *, context: Mapping[str, Any]
    ) -> None:
        self._email_service.send_email(
            email_template=CONTACT_OUTBOUND_EMAIL,
            to=[context["email"]],
            context=context,
        )
