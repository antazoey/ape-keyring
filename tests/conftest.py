import keyring.backend
import pytest
from ape import accounts
from ape._cli import cli as root_cli
from click.testing import CliRunner

from ape_keyring.testing import MockBackend


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
    return accounts.test_accounts[0]
