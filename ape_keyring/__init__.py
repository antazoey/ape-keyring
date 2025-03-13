from pathlib import Path

import ape.plugins

import ape_keyring._secrets


@ape.plugins.register(ape.plugins.Config)
def config_class():
    from .config import KeyringConfig

    return KeyringConfig


@ape.plugins.register(ape.plugins.AccountPlugin)
def account_types():
    from .accounts import KeyringAccount, KeyringAccountContainer

    return KeyringAccountContainer, KeyringAccount


def __getattr__(name):
    import ape_keyring._secrets

    return getattr(ape_keyring._secrets, name)


# TODO: Figure out how NOT to do this at plugin load time.
# Sync environment variables if configured to do so.
secret_manager = ape_keyring._secrets.get_secret_manager(Path.cwd())
secret_manager.set_environment_variables()

__all__ = ["Scope", "secret_manager"]
