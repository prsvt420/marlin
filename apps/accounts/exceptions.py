class AccountActivationError(Exception):
    pass


class AccountActivationLinkError(AccountActivationError):
    pass


class AccountActivationEmailError(AccountActivationError):
    pass


class AccountActivationEmailSendError(AccountActivationEmailError):
    pass
