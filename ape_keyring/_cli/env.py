import click
from ape import accounts
from ape.cli import ape_cli_context, non_existing_alias_argument

from ape_keyring.storage import environment_variable_storage
from ape_keyring.utils import get_address


@click.group()
def env():
    """Manage environment variables"""
    pass


@env.command("list")
@ape_cli_context()
def _list(cli_ctx):
    """
    List environments.
    """
    env_vars = environment_variable_storage.keys

    if not env_vars:
        cli_ctx.logger.warning("No environment variables found.")
        return

    num_variables = len(env_vars)
    click.echo(f"Found {num_variables} env-var{'s' if num_variables > 1 else ''}:")

    for var_key in env_vars:
        click.echo(f"  {var_key}")


@env.command(name="import")
@non_existing_alias_argument()
@ape_cli_context()
def _import(cli_ctx, alias):
    """
    Add a new keyfile account by entering a private key
    """
    key = click.prompt("Enter the private key", hide_input=True)
    address = get_address(key)
    if not address:
        cli_ctx.abort("Key could not be imported.")
        return

    container = accounts.containers["keyring"]
    container.create_account(alias, key)
    cli_ctx.logger.success(f"A new account '{address}' has been added with the ID '{alias}'.")
