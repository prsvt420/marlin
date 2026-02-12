from apps.core.dataclasses import EmailTemplate

SIGNIN_NOTIFICATION_EMAIL: EmailTemplate = EmailTemplate(
    subject="emails/signin_notification_subject.txt",
    body="emails/signin_notification.txt",
    content="emails/signin_notification.html",
)
PASSWORD_RESET_COMPLETE_EMAIL: EmailTemplate = EmailTemplate(
    subject="emails/password_reset_complete_subject.txt",
    body="emails/password_reset_complete.txt",
    content="emails/password_reset_complete.html",
)
ACCOUNT_ACTIVATION_EMAIL: EmailTemplate = EmailTemplate(
    subject="emails/account_activation_subject.txt",
    body="emails/account_activation.txt",
    content="emails/account_activation.html",
)
