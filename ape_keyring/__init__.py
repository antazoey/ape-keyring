import os

from ape import plugins

from .accounts import KeyringAccount, KeyringAccountContainer
from .config import KeyringConfig
from .storage import get_secret


@plugins.register(plugins.Config)
def config_class():
    return KeyringConfig


@plugins.register(plugins.AccountPlugin)
def account_types():
    return KeyringAccountContainer, KeyringAccount


def load_keyring_env():
    from ape import config

    env = config.get_config("keyring").env
    for var_name in env:
        secret = get_secret(var_name)
        if secret:
            os.environ[var_name] = secret
