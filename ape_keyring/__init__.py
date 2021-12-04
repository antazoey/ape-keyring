from ape import plugins

from .accounts import KeyringAccount, KeyringAccountContainer


@plugins.register(plugins.AccountPlugin)
def account_types():
    return KeyringAccountContainer, KeyringAccount
