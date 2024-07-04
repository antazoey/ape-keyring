from collections.abc import Iterator
from typing import Any, Optional

from ape.api import AccountAPI, AccountContainerAPI, TransactionAPI
from ape.exceptions import AccountsError
from ape.logging import logger
from ape.types import AddressType, MessageSignature, TransactionSignature
from ape.utils import cached_property
from eip712 import EIP712Message
from eth_account import Account as EthAccount
from eth_account.messages import SignableMessage, encode_defunct
from eth_pydantic_types import HexBytes
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
        return KeyringAccount(storage=self.storage, storage_key=alias, container=self)

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

    def sign_message(self, msg: Any, **signer_options) -> Optional[MessageSignature]:
        if isinstance(msg, str):
            msg = encode_defunct(text=msg)

        elif isinstance(msg, int):
            msg = encode_defunct(hexstr=HexBytes(msg).hex())

        elif isinstance(msg, bytes):
            msg = encode_defunct(primitive=msg)

        elif isinstance(msg, EIP712Message):
            # Display message data to user
            display_msg = "Signing EIP712 Message\n"

            # Domain Data
            display_msg += "Domain\n"
            if msg._name_:
                display_msg += f"\tName: {msg._name_}\n"
            if msg._version_:
                display_msg += f"\tVersion: {msg._version_}\n"
            if msg._chainId_:
                display_msg += f"\tChain ID: {msg._chainId_}\n"
            if msg._verifyingContract_:
                display_msg += f"\tContract: {msg._verifyingContract_}\n"
            if msg._salt_:
                display_msg += f"\tSalt: 0x{msg._salt_.hex()}\n"

            # Message Data
            display_msg += "Message\n"
            for field, value in msg._body_["message"].items():
                display_msg += f"\t{field}: {value}\n"

            # Convert EIP712Message to SignableMessage for handling below
            msg = msg.signable_message

        elif not isinstance(msg, SignableMessage):
            logger.warning("Unsupported message type, (type=%r, msg=%r)", type(msg), msg)
            return None

        signed_msg = EthAccount.sign_message(msg, self.__key)
        return MessageSignature(
            v=signed_msg.v,
            r=to_bytes(signed_msg.r),
            s=to_bytes(signed_msg.s),
        )

    def sign_transaction(self, txn: TransactionAPI, **signer_options) -> Optional[TransactionAPI]:
        if not self.__autosign and not agree_to_sign(txn, "transaction"):
            return None

        signed_txn = EthAccount.sign_transaction(
            txn.model_dump(by_alias=True, mode="json"), self.__key
        )
        txn.signature = TransactionSignature(
            v=signed_txn.v, r=to_bytes(signed_txn.r), s=to_bytes(signed_txn.s)
        )
        return txn

    def set_autosign(self, enabled: bool):
        """
        Allow this account to automatically sign messages and transactions.

        Args:
            enabled (bool): ``True`` to enable, ``False`` to disable.
        """
        logger.warning("Danger! This account will now sign any transaction it's given.")
        self.__autosign = enabled
