from typing import Optional

from ape.convert import to_address
from ape.logging import logger
from ape.types import AddressType
from eth_account import Account as EthAccount  # type: ignore
from eth_utils import to_bytes


def get_address(private_key: str) -> Optional[AddressType]:
    try:
        account = EthAccount.from_key(to_bytes(hexstr=private_key))
        return to_address(account.address)
    except Exception as err:
        logger.log_error(err)
        return None
