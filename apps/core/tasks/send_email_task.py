from smtplib import SMTPException
from typing import List

from celery import shared_task
from django.core.mail import EmailMultiAlternatives


@shared_task(
    bind=True,
    default_retry_delay=300,
    max_retries=5,
    autoretry_for=(SMTPException, OSError),
)
def send_email_task(
    self,
    *,
    subject: str,
    body: str,
    content: str,
    from_email: str,
    to: List[str],
) -> None:
    email_message: EmailMultiAlternatives = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=from_email,
        to=to,
    )
    email_message.attach_alternative(content=content, mimetype="text/html")
    email_message.send()
