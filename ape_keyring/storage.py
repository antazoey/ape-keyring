from typing import List

import keyring

_PRODUCT = "eth-ape"


class AccountStorage:
    ALIAS_LIST_KEY = "ape-keyring-aliases"

    @property
    def _account_keys_str(self) -> str:
        return get_secret(self.ALIAS_LIST_KEY) or ""

    @property
    def account_keys(self) -> List[str]:
        """
        The account aliases managed by the ``ape-keyring`` plugin.

        Returns:
            List[str]
        """
        return [k for k in self._account_keys_str.split(",") if k]

    def create_account(self, key: str, secret: str):
        """
        Add an account to the keyring storage.

        Args:
            key (str): The account key for look-up, e.g. the alias.
            secret (str): The account's private key.
        """
        self._append_new_account_key(key)
        set_secret(key, secret)

    def get_account(self, key: str) -> str:
        return get_secret(key)

    def delete_account(self, key: str):
        delete_secret(key)
        self._remove_account_key(key)

    def _append_new_account_key(self, new_key: str):
        new_value = f"{self._account_keys_str},{new_key}" if self._account_keys_str else new_key
        set_secret(self.ALIAS_LIST_KEY, new_value)

    def _remove_account_key(self, key: str):
        new_value = ",".join([k for k in self.account_keys if k != key])
        set_secret(self.ALIAS_LIST_KEY, new_value)


def get_secret(key: str) -> str:
    return keyring.get_password(_PRODUCT, key)


def set_secret(key: str, secret: str):
    keyring.set_password(_PRODUCT, key, secret)


def delete_secret(key: str):
    keyring.delete_password(_PRODUCT, key)
