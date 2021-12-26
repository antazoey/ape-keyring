from typing import List

import click
from ape import project
from ape.cli import ape_cli_context

from ape_keyring.args import existing_secret_argument, project_option, secret_argument
from ape_keyring.storage import secret_storage


@click.group()
def secrets():
    """Manage secrets"""


@secrets.command("list")
@ape_cli_context()
def _list(cli_ctx):
    """List secrets"""

    project_key = f"<<project={project.path.stem}>>"
    project_secrets = [k.replace(project_key, "") for k in secret_storage.keys if project_key in k]
    global_secrets = [
        k for k in secret_storage.keys if k not in project_secrets and "<<project=" not in k
    ]

    if not global_secrets and not project_secrets:
        cli_ctx.logger.warning("No secrets found.")
        return

    def output_secret_list(header: str, secret_keys: List[str]):
        if not secret_keys:
            return False

        click.echo(f"{header}:")
        for key in secret_keys:
            click.echo(f"  {key}")

        return True

    did_output = output_secret_list("Global secrets", global_secrets)
    if did_output and project_secrets:
        click.echo()

    output_secret_list("Project secrets", project_secrets)


@secrets.command(name="set")
@secret_argument()
@ape_cli_context()
@project_option()
def _set(cli_ctx, secret, project):
    """Add or repla ce a secret"""

    value = click.prompt(f"Enter the secret value for '{secret}'", hide_input=True)
    key = f"{secret}<<project={project}>>" if project else secret
    secret_storage.store_secret(key, value)
    cli_ctx.logger.success(f"Secret '{secret}' has been set.")


@secrets.command()
@ape_cli_context()
@existing_secret_argument()
def unset(cli_ctx, secret):
    """Remove a secret"""

    secret_storage.delete_secret(secret)
    cli_ctx.logger.success(f"Secret '{secret}' has been unset.")
