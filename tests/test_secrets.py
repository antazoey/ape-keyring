import os
from pathlib import Path

import ape
import pytest

from ape_keyring import Scope, secret_manager
from ape_keyring.config import KeyringConfig

SECRET_KEY = "TEST_SECRET"
SECRET_VALUE = "this-is-a-test-secret"


@pytest.fixture
def temp_global_secret():
    if SECRET_KEY not in secret_manager.keys:
        secret_manager.store_secret(SECRET_KEY, SECRET_VALUE)

    yield

    if SECRET_KEY in secret_manager.keys:
        secret_manager.delete_secret(SECRET_KEY)


@pytest.fixture(scope="session")
def config():
    return ape.config


@pytest.fixture(scope="session", autouse=True)
def from_tests_directory(config):
    with config.using_project(Path(__file__).parent):
        yield


def test_set(cli, runner):
    if SECRET_KEY in secret_manager.keys:
        # Corrupted from previous test.
        secret_manager.delete_secret(SECRET_KEY)

    result = runner.invoke(cli, ["keyring", "secrets", "set", SECRET_KEY], input=SECRET_VALUE)
    assert result.exit_code == 0, result.output


def test_list(cli, runner, temp_global_secret):
    result = runner.invoke(cli, ["keyring", "secrets", "list"])
    assert SECRET_KEY in result.output


def test_delete(cli, runner, temp_global_secret):
    result = runner.invoke(cli, ["keyring", "secrets", "delete", SECRET_KEY])
    assert result.exit_code == 0, result.output

    result = runner.invoke(cli, ["keyring", "secrets", "list"])
    assert SECRET_KEY not in result.output


def test_config(config):
    plugin_config = config.get_config("keyring")
    assert isinstance(plugin_config, KeyringConfig)
    assert plugin_config.set_env_vars is True


def test_secret_shows_in_env_var():
    if SECRET_KEY in secret_manager.keys:
        secret_manager.delete_secret(SECRET_KEY, scope=Scope.PROJECT)

    assert os.environ.get(SECRET_KEY) is None, f"{SECRET_KEY} found in env"
    secret_manager.store_secret(SECRET_KEY, SECRET_VALUE, scope=Scope.PROJECT)
    assert os.environ.get(SECRET_KEY) == SECRET_VALUE
