from dataclasses import dataclass


@dataclass(frozen=True)
class EmailTemplate:
    subject: str
    body: str
    content: str
