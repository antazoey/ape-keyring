from ape.exceptions import AccountsError, ApeException


class ApeKeyringException(ApeException):
    """
    A base error for the ape ``ape-keyring`` plugin.
    """


class ApeKeyringAccountError(ApeKeyringException, AccountsError):
    """
    A base error related to accounts in the ``ape-keyring`` plugin.
    """


class EmptyAliasError(ApeKeyringAccountError):
    def __init__(self):
        super().__init__("Alias cannot be empty.")


class SecretNotExistsError(ApeKeyringException):
    """
    Raised when trying to use a secret that does not exist.
    """

    def __init__(self, env_var_key: str):
        super().__init__(f"Secret '{env_var_key}' does not exist.")


class MissingSecretError(ApeKeyringException):
    """
    Raised when a secret was deleted outside of this plugin.
    """

    def __init__(self, alias: str):
        super().__init__(f"Missing secret for account with alias '{alias}'.")
