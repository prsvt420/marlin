from typing import TypedDict


class ContactContext(TypedDict):
    """Data context for handling a contact form.

    name (str): Full name of the user.
    email (str): User's email address.
    phone (str): User's phone number.
    subject (str): Subject or topic of the message.
    message (str): The main text body of the user's message.
    """

    name: str
    email: str
    phone: str
    subject: str
    message: str
