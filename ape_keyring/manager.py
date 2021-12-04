import keyring

_PRODUCT = "eth-ape"


def get_secret(key: str) -> str:
    return keyring.get_password(_PRODUCT, key)


def set_secret(key: str, secret: str):
    keyring.set_password(_PRODUCT, key, secret)


def delete_secret(key: str):
    keyring.delete_password(_PRODUCT, key)
