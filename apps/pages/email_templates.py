from apps.core.dataclasses import EmailTemplate

CONTACT_INBOUND_EMAIL: EmailTemplate = EmailTemplate(
    subject="emails/contact_inbound_subject.txt",
    body="emails/contact_inbound.txt",
    content="emails/contact_inbound.html",
)

CONTACT_OUTBOUND_EMAIL: EmailTemplate = EmailTemplate(
    subject="emails/contact_outbound_subject.txt",
    body="emails/contact_outbound.txt",
    content="emails/contact_outbound.html",
)
