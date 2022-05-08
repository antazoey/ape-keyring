import pytest
from ape import accounts
from eth_account import Account
from eth_account.messages import encode_defunct

TEST_ALIAS = "test-alias"


@pytest.fixture
def container():
    return accounts.containers["keyring"]


@pytest.fixture
def temp_keyfile_account(container, test_account):
    if TEST_ALIAS not in container.aliases:
        container.create_account(TEST_ALIAS, test_account.private_key)

    yield container.load(TEST_ALIAS)

    if TEST_ALIAS in container.aliases:
        container.delete_account(TEST_ALIAS)


def test_import(cli, runner, test_account, container):
    private_key = test_account.private_key
    result = runner.invoke(cli, ["keyring", "accounts", "import", TEST_ALIAS], input=private_key)
    assert not result.exit_code, result.output
    assert "SUCCESS" in result.output
    assert test_account.address in result.output
    container.delete_account(TEST_ALIAS)


def test_list(cli, runner, temp_keyfile_account):
    result = runner.invoke(cli, ["keyring", "accounts", "list"])
    assert temp_keyfile_account.address in result.output
    assert TEST_ALIAS in result.output


def test_sign_message(temp_keyfile_account):
    eip191message = encode_defunct(text="Hello Test")
    account = accounts.load(TEST_ALIAS)
    account.skip_prompt = True
    signature = account.sign_message(eip191message)
    signature_bytes = signature.encode_rsv()
    signer = Account.recover_message(eip191message, signature=signature_bytes)
    assert signer == temp_keyfile_account.address


def test_delete(cli, runner, temp_keyfile_account):
    result = runner.invoke(cli, ["keyring", "accounts", "delete", TEST_ALIAS])
    assert f"SUCCESS: Account '{TEST_ALIAS}' removed from keying" in result.output

    # Verify account is NOT listed in 'list' command
    result = runner.invoke(cli, ["keyring", "accounts", "list"])
    assert TEST_ALIAS not in result.output
