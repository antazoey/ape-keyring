import os
from enum import Enum
from pathlib import Path
from typing import List, Union

from ape.managers.config import CONFIG_FILE_NAME
from ape.utils import extract_nested_value, load_config

from ape_keyring.config import KeyringConfig
from ape_keyring.storage import SecretStorage, secret_storage


class Scope(Enum):
    GLOBAL = "global"
    PROJECT = "project"


class SecretManager:
    def __init__(self, project_path: Path, storage: SecretStorage, config: KeyringConfig):
        self._path = project_path
        self._storage = storage
        self._config = config

    def set_environment_variables(self):
        """
        Set the environment variables if told to from the config.
        """
        if not self._set_environment_variables:
            return

        for key, value in self._storage:
            self._set(key, value)

    @property
    def project_name(self) -> str:
        return self._path.stem

    @property
    def _project_key_prefix(self) -> str:
        return "<<project="

    @property
    def _project_key(self):
        return f"{self._project_key_prefix}{self.project_name}>>"

    @property
    def secrets_exist(self) -> bool:
        return self.project_secrets or self.global_secrets  # type: ignore

    @property
    def project_secrets(self) -> List[str]:
        keys = self._storage.keys
        return [k.replace(self._project_key, "") for k in keys if self._project_key in k]

    @property
    def global_secrets(self) -> List[str]:
        keys = self._storage.keys
        return [
            k for k in keys if k not in self.project_secrets and self._project_key_prefix not in k
        ]

    @property
    def _set_environment_variables(self) -> bool:
        return extract_nested_value(self._config, "keyring", "set_env_vars") or False

    def get_secret(self, key, scope: Union[str, Scope] = Scope.GLOBAL) -> str:
        scope = Scope(scope)
        key = self._get_key(key, scope)
        return self._storage.get_secret(key) or ""

    def store_secret(self, key: str, secret: str, scope: Union[str, Scope] = Scope.GLOBAL):
        scope = Scope(scope)
        key = self._get_key(key, scope)
        self._storage.store_secret(key, secret)
        if self._set_environment_variables:
            self._set(key, secret)

    def delete_secret(self, key: str, scope: Union[str, Scope] = Scope.GLOBAL) -> bool:
        scope = Scope(scope)
        key = self._get_key(key, scope)
        did_delete = self._storage.delete_secret(key)
        if self._set_environment_variables:
            self._unset(key)

        return did_delete

    def _get_key(self, key: str, scope: Scope):
        return f"{key}{self._project_key}" if scope == Scope.PROJECT else key

    def _set(self, key: str, value: str):
        # Strip of 'project=' and '<<>>' parts before setting as env var.
        key = self._extract_env_var_key(key)
        os.environ[key] = value

    def _unset(self, key: str):
        key = self._extract_env_var_key(key)
        del os.environ[key]

    def _extract_env_var_key(self, key: str):
        return key.split(self._project_key)[0]


def get_secret_manager(project_path: Path):
    config = load_config(Path(CONFIG_FILE_NAME)) or {}
    return SecretManager(project_path, secret_storage, config)  # type: ignore


__all__ = ["get_secret_manager", "Scope", "SecretManager"]
