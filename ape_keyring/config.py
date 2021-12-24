from typing import List

from ape.api import ConfigItem


class KeyringConfig(ConfigItem):
    env: List[str] = []
