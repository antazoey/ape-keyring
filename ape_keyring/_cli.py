import click
from ape import accounts
from ape.cli import ape_cli_context, existing_alias_argument, non_existing_alias_argument

from ape_keyring.accounts import KeyringAccount
from ape_keyring.utils import get_address

container = accounts.containers["keyring"]


@click.group("keyring")
def cli():
    """Manage accounts and secrets"""
    pass


@cli.group("accounts")
def account_cli():
    """Manage accounts"""
    pass


@account_cli.command("list")
@ape_cli_context()
def _list(cli_ctx):
    """
    List keyring accounts.
    """
    keyring_accounts = [a for a in accounts if isinstance(a, KeyringAccount)]

    if len(keyring_accounts) == 0:
        cli_ctx.logger.warning("No accounts found.")
        return

    num_accounts = len(accounts)
    header = f"Found {num_accounts} account"
    header += "s:" if num_accounts > 1 else ":"
    click.echo(header)

    for account in keyring_accounts:
        alias_display = f" (alias: '{account.alias}')" if account.alias else ""
        click.echo(f"  {account.address}{alias_display}")


@account_cli.command(name="import")
@non_existing_alias_argument()
@ape_cli_context()
def _import(cli_ctx, alias):
    """
    Add a new keyfile account by entering a private key
    """
    key = click.prompt("Enter Private Key", hide_input=True)
    address = get_address(key)
    if not address:
        cli_ctx.abort("Key could not be imported.")
        return

    container.create_account(alias, key)
    cli_ctx.logger.success(f"A new account '{address}' has been added with the ID '{alias}'.")


@account_cli.command()
@ape_cli_context()
@existing_alias_argument()
def delete(cli_ctx, alias):
    """
    Delete an account from keyring
    """
    container.delete_account(alias)
    cli_ctx.logger.success(f"Account '{alias}' removed from keying.")


@account_cli.command()
@ape_cli_context()
def delete_all(cli_ctx):
    """
    Delete all keyring accounts
    """
    container.delete_all()
    cli_ctx.logger.success("Deleted all keyring accounts.")
