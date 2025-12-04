from typing import TypedDict


class ContactContext(TypedDict):
    """Data context for handling a contact form.

    full_name (str): Full name of the user.
    email (str): User's email address.
    phone_number (str): User's phone number.
    subject (str): Subject or topic of the message.
    message (str): The main text body of the user's message.
    """

    full_name: str
    email: str
    phone_number: str
    subject: str
    message: str
