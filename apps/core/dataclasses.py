from dataclasses import dataclass


@dataclass(frozen=True)
class EmailTemplate:
    """Data structure for email templates."""

    subject: str
    body: str
    content: str
