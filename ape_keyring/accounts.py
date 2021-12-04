import json
from pathlib import Path
from typing import Dict, Iterator, Optional

import click
from ape.api import AccountAPI, AccountContainerAPI, TransactionAPI
from ape.convert import to_address
from ape.exceptions import AccountsError
from ape.types import AddressType, MessageSignature, TransactionSignature
from eth_account import Account as EthAccount  # type: ignore
from eth_account.messages import SignableMessage
from eth_utils import to_bytes

from ape_keyring.manager import delete_secret, get_secret, set_secret


class KeyringAccountContainer(AccountContainerAPI):
    @property
    def _account_files(self) -> Iterator[Path]:
        return self.data_folder.glob("*.json")

    @property
    def aliases(self) -> Iterator[str]:
        for p in self._account_files:
            yield p.stem

    def load(self, alias: str) -> "KeyringAccount":
        for account_alias in self._account_files:
            if alias == account_alias:
                return KeyringAccount(self, alias)

        raise AccountsError(f"No keyring account named '{alias}'.")

    def __len__(self) -> int:
        return len([*self._account_files])

    def __iter__(self) -> Iterator[AccountAPI]:
        for alias in self._account_files:
            yield KeyringAccount(self, alias)  # type: ignore

    def __setitem__(self, address: AddressType, account: AccountAPI):
        pass

    def __delitem__(self, address: AddressType):
        pass

    def create_account(self, alias: str, key: str, passphrase: Optional[str] = None):
        path = self.data_folder.joinpath(f"{alias}.json")
        account = EthAccount.from_key(to_bytes(hexstr=key))
        set_secret(alias, key)
        path.write_text(
            json.dumps({"address": account.address, "uses_passphrase": passphrase is not None})
        )
        set_secret(alias, key, passphrase=passphrase)

    def delete_account(self, alias: str, passphrase: Optional[str] = None):
        account = KeyringAccount(self, alias)

        if account.uses_passphrasea and passphrase is None:
            raise AccountsError("Passphrase required.")

        account.path.unlink(missing_ok=True)
        delete_secret(alias, passphrase=passphrase)


class KeyringAccount(AccountAPI):
    _account_file: Path

    @property
    def path(self) -> Path:
        return self._account_file

    @property
    def account_file(self) -> Dict:
        return json.loads(self._account_file.read_text())

    @property
    def alias(self) -> str:
        return self._account_file.stem

    @property
    def uses_passphrase(self) -> bool:
        return self.account_file["uses_passphrase"]

    @property
    def address(self) -> AddressType:
        return to_address(self.account_file["address"])

    @property
    def __key(self) -> str:
        passphrase = (
            click.prompt(f"Account passphrase for '{self.alias}'") if self.uses_passphrase else None
        )
        return get_secret(self.alias, passphrase=passphrase)

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
