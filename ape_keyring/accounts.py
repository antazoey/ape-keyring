from typing import Iterator, Optional

from ape.api import AccountAPI, AccountContainerAPI, TransactionAPI
from ape.types import AddressType, MessageSignature, TransactionSignature
from ape.utils import cached_property
from eth_account import Account as EthAccount  # type: ignore
from eth_account.messages import SignableMessage
from eth_utils import to_bytes

from ape_keyring.exceptions import EmptyAliasError, MissingSecretError
from ape_keyring.storage import account_storage
from ape_keyring.utils import agree_to_sign, get_address


class KeyringAccountContainer(AccountContainerAPI):
    @property
    def aliases(self) -> Iterator[str]:
        for alias in account_storage.keys:
            if alias:
                yield alias

    def load(self, alias: str) -> "KeyringAccount":
        return KeyringAccount(_alias=alias, container=self)  # type: ignore

    def __len__(self) -> int:
        return len([a for a in self.aliases if a])

    def __iter__(self) -> Iterator[AccountAPI]:
        for alias in self.aliases:
            if alias:
                yield KeyringAccount(_alias=alias, container=self)  # type: ignore

    def __setitem__(self, address: AddressType, account: AccountAPI):
        pass

    def __delitem__(self, address: AddressType):
        pass

    def create_account(self, alias: str, secret: str):
        if not alias:
            raise EmptyAliasError()

        account_storage.store_secret(alias, secret)

    def delete_account(self, alias: str):
        if not alias:
            raise EmptyAliasError()

        account_storage.delete_secret(alias)

    def delete_all(self):
        account_storage.delete_all()


class KeyringAccount(AccountAPI):
    _alias: str
    _address: Optional[AddressType] = None
    skip_prompt: bool = False

    @property
    def alias(self) -> str:
        return self._alias

    @cached_property
    def address(self) -> AddressType:
        if not self._address:
            self._address = get_address(self.__key)

        assert self._address is not None  # for mypy
        return self._address

    @property
    def __key(self) -> str:
        key = account_storage.get_secret(self._alias)
        if not key:
            raise MissingSecretError(self._alias)

        return key

    def sign_message(self, msg: SignableMessage) -> Optional[MessageSignature]:
        if not self.skip_prompt and not agree_to_sign(msg, "message"):
            return None

        signed_msg = EthAccount.sign_message(msg, self.__key)
        return MessageSignature(
            v=signed_msg.v, r=to_bytes(signed_msg.r), s=to_bytes(signed_msg.s)
        )  # type: ignore

    def sign_transaction(self, txn: TransactionAPI) -> Optional[TransactionSignature]:
        if not self.skip_prompt and not agree_to_sign(txn, "transaction"):
            return None

        signed_txn = EthAccount.sign_transaction(txn.as_dict(), self.__key)
        return TransactionSignature(
            v=signed_txn.v, r=to_bytes(signed_txn.r), s=to_bytes(signed_txn.s)
        )  # type: ignore
