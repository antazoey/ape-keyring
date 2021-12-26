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


class SecretAlreadyStoredError(ApeKeyringException):
    """
    Raised when trying to store an already existing secret.
    """

    def __init__(self, env_var_key: str):
        super().__init__(f"Environment variable '${env_var_key}' already stored.")


class MissingSecretError(ApeKeyringException):
    """
    Raised when a secret was deleted outside of this plugin.
    """

    def __init__(self, alias: str):
        super().__init__(f"Missing secret for account with alias '{self._alias}'.")
