from pathlib import Path

from ape import plugins

from .accounts import KeyringAccount, KeyringAccountContainer
from .config import KeyringConfig
from .secrets import get_secret_manager


@plugins.register(plugins.Config)
def config_class():
    return KeyringConfig


@plugins.register(plugins.AccountPlugin)
def account_types():
    return KeyringAccountContainer, KeyringAccount


# Sync environment variables if configured to do so.
get_secret_manager(Path.cwd()).set_environment_variables()
