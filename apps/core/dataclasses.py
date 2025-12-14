from dataclasses import dataclass


@dataclass(frozen=True)
class EmailTemplate:
    """Container for email templates.

    Attributes:
        subject (str): Path to the template file for the email subject.
        body (str): Path to the template file for the plain text
        body of the email.
        content (str): Path to the template file for the HTML content
        of the email.
    """

    subject: str
    body: str
    content: str
