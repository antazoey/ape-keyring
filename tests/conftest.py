from pathlib import Path

import ape
import keyring.backend
import pytest
from ape._cli import cli as root_cli
from click.testing import CliRunner

from ape_keyring.testing import MockBackend


@pytest.fixture(scope="session")
def config():
    return ape.config


@pytest.fixture(scope="session", autouse=True)
def from_tests_directory(config):
    with config.using_project(Path(__file__).parent):
        yield


@pytest.fixture(autouse=True)
def mock_keyring_backend():
    keyring.set_keyring(MockBackend())


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def cli():
    return root_cli


@pytest.fixture
def test_account():
    return ape.accounts.test_accounts[0]
