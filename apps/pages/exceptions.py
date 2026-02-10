class ContactEmailSendError(Exception):
    pass


class ContactInboundEmailSendError(ContactEmailSendError):
    pass


class ContactOutboundEmailSendError(ContactEmailSendError):
    pass
