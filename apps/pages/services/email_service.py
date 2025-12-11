from typing import List

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django_stubs_ext import StrOrPromise

from apps.pages.types import ContactContext
from config import settings


class EmailService:
    """Service for sending emails."""

    def __init__(self, from_email: str = settings.DEFAULT_FROM_EMAIL) -> None:
        """Initialize the email service with a sender email.

        Args:
            from_email (str): Email address to use as sender.
                Defaults to settings.DEFAULT_FROM_EMAIL if not provided.
        """
        self.from_email: str = from_email

    def send_email(
        self,
        subject: StrOrPromise,
        to: List[str],
        template_name: str,
        contact_context: ContactContext,
        body: str = "",
    ) -> None:
        """Send an email with HTML content rendered from a template.

        Args:
            subject (StrOrPromise): Subject of the email.
            to (List[str]): List of recipient email addresses.
            template_name (str): Path to the email template.
            contact_context (ContactContext): Context data for rendering
            the template.
            body (str): Plain text body of the email. Defaults
            to empty string.
        """
        content: str = render_to_string(
            template_name=template_name, context=contact_context
        )

        email_message: EmailMultiAlternatives = EmailMultiAlternatives(
            subject=subject,
            body=body,
            from_email=self.from_email,
            to=to,
        )

        email_message.attach_alternative(content=content, mimetype="text/html")

        email_message.send()

    def send_contact_message(self, contact_context: ContactContext) -> None:
        """Send a contact message to the site admin.

        Args:
            contact_context (ContactContext): Data from the contact form,
                including sender info and message content.
        """
        body: str = render_to_string(
            template_name="emails/contact_message.html"
        )
        subject: str = render_to_string(
            template_name="emails/contact_message_subject.txt"
        ).strip()
        self.send_email(
            subject=subject,
            to=[settings.DEFAULT_FROM_EMAIL],
            template_name="emails/contact_message.html",
            contact_context=contact_context,
            body=body,
        )

    def send_contact_reply(self, contact_context: ContactContext) -> None:
        """Send an reply to the user.

        Args:
            contact_context (ContactContext): Data from the contact form,
                including sender's email to reply to.
        """
        body: str = render_to_string(template_name="emails/contact_reply.html")
        subject: str = render_to_string(
            template_name="emails/contact_reply_subject.txt"
        ).strip()
        self.send_email(
            subject=subject,
            to=[contact_context["email"]],
            template_name="emails/contact_reply.html",
            contact_context=contact_context,
            body=body,
        )
