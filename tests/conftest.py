import ape
import keyring.backend
import pytest
from ape._cli import cli as root_cli
from click.testing import CliRunner

from ape_keyring._secrets import get_secret_manager
from ape_keyring.storage import SecretStorage
from ape_keyring.testing import EphemeralBackend


@pytest.fixture(scope="session", autouse=True)
def config():
    with ape.config.isolate_data_folder():
        yield ape.config


@pytest.fixture(scope="session", autouse=True)
def project():
    return ape.project


@pytest.fixture(scope="session", autouse=True)
def backend(accounts):
    backend = EphemeralBackend()
    keyring.set_keyring(backend)
    return backend


@pytest.fixture(scope="session", autouse=True)
def storage():
    return SecretStorage("secrets")


@pytest.fixture(scope="session", autouse=True)
def secret_manager(container, storage, project):
    return get_secret_manager(project.path, storage=storage)


@pytest.fixture(scope="session", autouse=True)
def container(accounts, storage):
    container = accounts.containers["keyring"]
    container.storage = storage
    return container


@pytest.fixture(scope="session")
def accounts():
    return ape.accounts


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture(scope="session")
def cli():
    return root_cli


@pytest.fixture(scope="session")
def existing_alias():
    return "existing-test-alias"


@pytest.fixture(scope="session")
def non_existing_alias():
    return "non_existing-test-alias"


@pytest.fixture
def test_account(accounts):
    return accounts.test_accounts[0]


@pytest.fixture
def address(test_account):
    return test_account.address


@pytest.fixture
def private_key(test_account):
    return test_account.private_key


@pytest.fixture
def keyring_account(container, private_key, existing_alias):
    if existing_alias not in container.aliases:
        container.create_account(existing_alias, private_key)

    yield container.load(existing_alias)

    if existing_alias in container.aliases:
        container.delete_account(existing_alias)
