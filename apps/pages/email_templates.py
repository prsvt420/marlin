from apps.core.dataclasses import EmailTemplate

CONTACT_MESSAGE: EmailTemplate = EmailTemplate(
    subject="emails/contact_message_subject.txt",
    body="emails/contact_message.txt",
    content="emails/contact_message.html",
)
CONTACT_REPLY: EmailTemplate = EmailTemplate(
    subject="emails/contact_reply_subject.txt",
    body="emails/contact_reply.txt",
    content="emails/contact_reply.html",
)
