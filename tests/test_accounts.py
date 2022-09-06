import pytest
from eth_account import Account
from eth_account.messages import encode_defunct


@pytest.fixture
def eip191_message():
    return encode_defunct(text="Hello Test")


def test_import(cli, runner, test_account, container, non_existing_alias):
    result = runner.invoke(
        cli, ["keyring", "accounts", "import", non_existing_alias], input=test_account.private_key
    )
    assert not result.exit_code, result.output
    assert "SUCCESS" in result.output
    assert test_account.address in result.output
    container.delete_account(non_existing_alias)


def test_list(cli, runner, keyring_account, existing_alias):
    result = runner.invoke(cli, ["keyring", "accounts", "list"])
    assert result.exit_code == 0, result.output
    assert existing_alias in result.output


def test_sign_message(keyring_account, runner, eip191_message):
    with runner.isolation("y\n"):
        signature = keyring_account.sign_message(eip191_message)

    signature_bytes = signature.encode_rsv()
    signer = Account.recover_message(eip191_message, signature=signature_bytes)
    assert signer == keyring_account.address


def test_set_autosign(keyring_account, eip191_message, runner):
    keyring_account.set_autosign(True)

    # The password is not required
    keyring_account.sign_message(eip191_message)

    keyring_account.set_autosign(False)

    # The password is now required
    with runner.isolation("y\n"):
        keyring_account.sign_message(eip191_message)


def test_delete(cli, runner, keyring_account):
    result = runner.invoke(cli, ["keyring", "accounts", "delete", keyring_account.alias])
    assert f"SUCCESS: Account '{keyring_account.alias}' removed from keying" in result.output

    # Verify account is NOT listed in 'list' command
    result = runner.invoke(cli, ["keyring", "accounts", "list"])
    assert keyring_account.alias not in result.output
