import os
from contextlib import contextmanager
from pathlib import Path

import ape
import pytest

from ape_keyring import Scope, secret_manager
from ape_keyring.config import KeyringConfig

GLOBAL_SECRET_KEY = "__GLOBAL_TEST_SECRET__"
PROJECT_SECRET_KEY = "__PROJECT_TEST_SECRET__"
GLOBAL_SECRET_VALUE = "test-global-secret-value"
PROJECT_SECRET_VALUE = "test-project-secret-value"

key_value_and_scope = pytest.mark.parametrize(
    "key,value,scope",
    [
        (GLOBAL_SECRET_KEY, GLOBAL_SECRET_VALUE, Scope.GLOBAL.value),
        (PROJECT_SECRET_KEY, PROJECT_SECRET_VALUE, Scope.PROJECT.value),
    ],
)


@pytest.fixture(scope="module", autouse=True)
def auto_clean():
    yield

    for key in [GLOBAL_SECRET_KEY, PROJECT_SECRET_KEY]:
        if key in secret_manager.keys:
            secret_manager.delete_secret(key)


@pytest.fixture(scope="session")
def config():
    return ape.config


@pytest.fixture(scope="session", autouse=True)
def from_tests_directory(config):
    with config.using_project(Path(__file__).parent):
        yield


@pytest.fixture
def temp_global_secret():
    with set_temp_secret(GLOBAL_SECRET_KEY, GLOBAL_SECRET_VALUE, Scope.GLOBAL):
        yield


@pytest.fixture
def temp_project_secret():
    with set_temp_secret(PROJECT_SECRET_KEY, PROJECT_SECRET_VALUE, Scope.PROJECT):
        yield


@pytest.fixture
def temp_secrets(temp_global_secret, temp_project_secret):
    yield


@contextmanager
def set_temp_secret(key: str, value: str, scope: Scope):
    if key not in secret_manager.keys:
        secret_manager.store_secret(key, value, scope=scope)

    yield


@key_value_and_scope
def test_set(cli, runner, key, value, scope):
    if key in secret_manager.keys:
        # Corrupted from previous test.
        secret_manager.delete_secret(key, scope=scope)

    result = runner.invoke(cli, ["keyring", "secrets", "set", key, "--scope", scope], input=value)
    assert result.exit_code == 0, result.output

    opposite = [k for k in [GLOBAL_SECRET_KEY, PROJECT_SECRET_KEY] if k != key][0]
    assert key in secret_manager.keys
    assert opposite not in secret_manager.keys
    secret_manager.delete_secret(key, scope=scope)


@pytest.mark.parametrize("key", (GLOBAL_SECRET_KEY, PROJECT_SECRET_KEY))
def test_list(cli, runner, temp_secrets, key):
    result = runner.invoke(cli, ["keyring", "secrets", "list"])
    assert key in result.output


@key_value_and_scope
def test_delete(cli, runner, temp_secrets, key, value, scope):
    _ = value
    result = runner.invoke(cli, ["keyring", "secrets", "delete", key, "--scope", scope])
    assert result.exit_code == 0, result.output

    result = runner.invoke(cli, ["keyring", "secrets", "list"])
    assert key not in result.output


def test_config(config):
    plugin_config = config.get_config("keyring")
    assert isinstance(plugin_config, KeyringConfig)
    assert plugin_config.set_env_vars is True


@key_value_and_scope
def test_secrets_in_env(temp_secrets, key, value, scope):
    if key in secret_manager.keys:
        secret_manager.delete_secret(key, scope=scope)

    secret_manager.store_secret(key, value, scope=scope)
    assert os.environ.get(key) == value
    secret_manager.delete_secret(key, scope=scope)
    assert not os.environ.get(key)
