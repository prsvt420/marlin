from django import forms


class ContactForm(forms.Form):
    """Form for collecting user contact information and message.

    This form is used to gather details from users who want to
    get in touch, including their name, email address, phone number,
    subject of the inquiry, and message content.

    Attributes:
        name (CharField): Full name of the user.
        email (EmailField): User's email address.
        phone (CharField): User's phone number.
        subject (CharField): Subject or topic of the message.
        message (CharField): The main text body of the user's message.
    """

    name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
