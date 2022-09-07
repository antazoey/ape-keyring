from typing import Iterator, Optional

from ape.api import AccountAPI, AccountContainerAPI, TransactionAPI
from ape.exceptions import AccountsError
from ape.logging import logger
from ape.types import AddressType, MessageSignature, TransactionSignature
from ape.utils import cached_property
from eth_account import Account as EthAccount  # type: ignore
from eth_account.messages import SignableMessage
from eth_utils import to_bytes

from ape_keyring.exceptions import EmptyAliasError, MissingSecretError
from ape_keyring.storage import SecretStorage, account_storage
from ape_keyring.utils import agree_to_sign, get_eth_account


class KeyringAccountContainer(AccountContainerAPI):
    storage: SecretStorage = account_storage

    @property
    def aliases(self) -> Iterator[str]:
        yield from [a for a in self.storage.keys if a]

    @property
    def accounts(self) -> Iterator[AccountAPI]:
        for alias in self.aliases:
            yield self.load(alias)

    def load(self, alias: str) -> "KeyringAccount":
        return KeyringAccount(
            storage=self.storage, storage_key=alias, container=self
        )  # type: ignore

    def __len__(self) -> int:
        return len([a for a in self.aliases if a])

    def create_account(self, alias: str, secret: str):
        if not alias:
            raise EmptyAliasError()

        self.storage.store_secret(alias, secret)
        if not self.storage.get_secret(alias):
            raise AccountsError(f"Failed to create account '{alias}'")

    def delete_account(self, alias: str):
        if not alias:
            raise EmptyAliasError()

        self.storage.delete_secret(alias)

    def delete_all(self):
        self.storage.delete_all()


class KeyringAccount(AccountAPI):
    storage: SecretStorage
    storage_key: str
    cached_address: Optional[AddressType] = None
    __autosign: bool = False

    def __repr__(self):
        return f"<{self.__class__.__name__} address={self.address} alias={self.alias}>"

    @property
    def alias(self) -> str:
        return self.storage_key

    @cached_property
    def address(self) -> AddressType:
        if not self.cached_address:
            eth_account = get_eth_account(self.__key)
            if eth_account:
                ethereum = self.network_manager.get_ecosystem("ethereum")
                self.cached_address = ethereum.decode_address(eth_account.address)

        if not self.cached_address:
            raise AccountsError("Account private key corrupted.")

        return self.cached_address

    @property
    def __key(self) -> str:
        key = self.storage.get_secret(self.storage_key)
        if not key:
            raise MissingSecretError(self.storage_key)

        return key

    def sign_message(self, msg: SignableMessage) -> Optional[MessageSignature]:
        if not self.__autosign and not agree_to_sign(msg, "message"):
            return None

        signed_msg = EthAccount.sign_message(msg, self.__key)
        return MessageSignature(
            v=signed_msg.v, r=to_bytes(signed_msg.r), s=to_bytes(signed_msg.s)
        )  # type: ignore

    def sign_transaction(self, txn: TransactionAPI) -> Optional[TransactionSignature]:
        if not self.__autosign and not agree_to_sign(txn, "transaction"):
            return None

        signed_txn = EthAccount.sign_transaction(txn.dict(), self.__key)
        return TransactionSignature(
            v=signed_txn.v, r=to_bytes(signed_txn.r), s=to_bytes(signed_txn.s)
        )  # type: ignore

    def set_autosign(self, enabled: bool):
        """
        Allow this account to automatically sign messages and transactions.

        Args:
            enabled (bool): ``True`` to enable, ``False`` to disable.
        """
        logger.warning("Danger! This account will now sign any transaction it's given.")
        self.__autosign = enabled
