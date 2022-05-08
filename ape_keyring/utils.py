from typing import Any, Optional

import click
from ape.logging import logger
from eth_account import Account as EthAccount  # type: ignore
from eth_account.signers.local import LocalAccount
from eth_utils import to_bytes


def get_eth_account(private_key: str) -> Optional[LocalAccount]:
    try:
        return EthAccount.from_key(to_bytes(hexstr=private_key))
    except Exception as err:
        logger.log_error(err)
        return None


def agree_to_sign(message: Any, message_type_name: str) -> bool:
    return click.confirm(f"Sign {message_type_name}: {message}")
