import os
from pathlib import Path

from ape import plugins
from ape.managers.config import CONFIG_FILE_NAME
from ape.utils import extract_nested_value, load_config

from .accounts import KeyringAccount, KeyringAccountContainer
from .config import KeyringConfig
from .storage import secret_storage


@plugins.register(plugins.Config)
def config_class():
    return KeyringConfig


@plugins.register(plugins.AccountPlugin)
def account_types():
    return KeyringAccountContainer, KeyringAccount


# Set the environment variables if told to from the config.
config = load_config(Path(CONFIG_FILE_NAME)) or {}
set_env_vars = extract_nested_value(config, "keyring", "set_env_vars") or False
current_project_name = Path.cwd().stem

if set_env_vars:
    for key, value in secret_storage:
        project_key = f"<<project={Path.cwd().stem}>>"
        key = key.split(project_key)[0]
        os.environ[key] = value
