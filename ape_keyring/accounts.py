from typing import Iterator, List, Optional

import click
from ape.api import AccountAPI, AccountContainerAPI, TransactionAPI
from ape.types import AddressType, MessageSignature, TransactionSignature
from ape.utils import cached_property
from eth_account import Account as EthAccount  # type: ignore
from eth_account.messages import SignableMessage

from ape_keyring.exceptions import EmptyAliasError
from ape_keyring.storage import AccountStorage
from ape_keyring.utils import get_address


class KeyringAccountContainer(AccountContainerAPI):
    storage: AccountStorage = AccountStorage()

    @property
    def aliases(self) -> List[str]:
        return [a for a in self.storage.account_keys if a]

    def load(self, alias: str) -> "KeyringAccount":
        return KeyringAccount(_storage_key=alias, container=self)

    def __len__(self) -> int:
        return len([a for a in self.aliases])

    def __iter__(self) -> Iterator[AccountAPI]:
        for alias in self.aliases:
            yield KeyringAccount(_storage_key=alias, container=self)  # type: ignore

    def __setitem__(self, address: AddressType, account: AccountAPI):
        pass

    def __delitem__(self, address: AddressType):
        pass

    def create_account(self, alias: str, secret: str):
        if not alias:
            raise EmptyAliasError()

        self.storage.create_account(alias, secret)

    def delete_account(self, alias: str):
        if not alias:
            raise EmptyAliasError()

        self.storage.delete_account(alias)


class KeyringAccount(AccountAPI):
    _storage_key: str
    _address: Optional[AddressType] = None

    @property
    def alias(self) -> str:
        return self._storage_key

    @cached_property
    def address(self) -> AddressType:
        if not self._address:
            self._address = get_address(self.__key)

        return self._address

    @property
    def __key(self) -> str:
        return self.container.storage.get_account(self._storage_key)

    def sign_message(self, msg: SignableMessage) -> Optional[MessageSignature]:
        if not click.confirm(f"{msg}\n\nSign: "):
            return None

        signed_msg = EthAccount.sign_message(msg, self.__key)
        return MessageSignature(v=signed_msg.v, r=signed_msg.r, s=signed_msg.s)  # type: ignore

    def sign_transaction(self, txn: TransactionAPI) -> Optional[TransactionSignature]:
        if not click.confirm(f"{txn}\n\nSign: "):
            return None

        signed_txn = EthAccount.sign_transaction(txn.as_dict(), self.__key)
        return TransactionSignature(v=signed_txn.v, r=signed_txn.r, s=signed_txn.s)  # type: ignore
