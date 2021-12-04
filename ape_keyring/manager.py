from typing import Optional

import keyring

_PRODUCT = "eth-ape"


def get_secret(key: str, passphrase: Optional[str] = None) -> str:
    source = _get_source_name(passphrase)
    return keyring.get_password(source, key)


def set_secret(key: str, secret: str, passphrase: Optional[str] = None):
    source = _get_source_name(passphrase)
    keyring.set_password(source, key, secret)


def delete_secret(key: str, passphrase: Optional[str] = None):
    source = _get_source_name(passphrase)
    keyring.delete_password(source, key)


def _get_source_name(passphrase: Optional[str] = None) -> str:
    return f"{_PRODUCT}-{passphrase}" if passphrase else _PRODUCT
