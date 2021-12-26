import click

from ape_keyring._cli.accounts import account_cli
from ape_keyring._cli.secrets import secrets


@click.group("keyring")
def cli():
    """Manage accounts and secrets"""
    pass


cli.add_command(account_cli)  # type: ignore
cli.add_command(secrets)  # type: ignore
