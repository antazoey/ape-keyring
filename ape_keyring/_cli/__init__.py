import click

from ape_keyring._cli.accounts import account_cli


@click.group("keyring")
def cli():
    """Manage accounts and secrets"""
    pass


cli.add_command(account_cli)
