from ape.exceptions import AccountsError


class ApeKeyringError(AccountsError):
    """
    Raised when there is an issue with the keyring storage.
    """


class EmptyAliasError(ApeKeyringError):
    def __init__(self):
        super().__init__("Alias cannot be empty.")
