import click
from ape import project

from ape_keyring.exceptions import SecretNotExistsError
from ape_keyring.storage import secret_storage


def secret_argument(callback=None):
    return click.argument("secret", callback=callback)


def existing_secret_argument():
    """
    A ``click.argument`` for a secret that exists in ape-keyring.
    """

    def _require_secret(value):
        if value not in secret_storage.keys:
            raise SecretNotExistsError()

        return value

    return secret_argument(callback=lambda ctx, param, value: _require_secret(value))


def project_option():
    return click.option(
        "--project",
        help="Set to scope the secret to the active project",
        is_flag=True,
        callback=lambda c, p, v: project.path.stem if v else None,
    )
