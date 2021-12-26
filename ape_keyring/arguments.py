import click
from ape import accounts

from ape_keyring.exceptions import SecretAlreadyStoredError


def _require_non_env_var(value):
    if value in accounts.aliases:
        raise SecretAlreadyStoredError(value)

    return value


def non_existing_env_var_argument():
    """
    A ``click.argument`` for an environment variable that does not yet exist in ape-keyring.
    """

    return click.argument("alias", callback=lambda ctx, param, value: _require_non_env_var(value))
