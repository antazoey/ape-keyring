import click

from ape_keyring.secrets import Scope


def secret_argument(callback=None):
    return click.argument("secret", callback=callback)


def scope_option():
    return click.option(
        "--scope",
        help="Set to 'project' to limit the scope to the current project.",
        default="global",
        callback=lambda ctx, param, value: Scope(value),
    )
