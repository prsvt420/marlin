class ContactEmailError(Exception):
    pass


class ContactEmailSendError(ContactEmailError):
    pass


class ContactInboundEmailSendError(ContactEmailSendError):
    pass


class ContactOutboundEmailSendError(ContactEmailSendError):
    pass
