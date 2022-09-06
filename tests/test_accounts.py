from eth_account import Account
from eth_account.messages import encode_defunct


def test_import(cli, runner, test_account, container, non_existing_alias):
    private_key = test_account.private_key
    result = runner.invoke(
        cli, ["keyring", "accounts", "import", non_existing_alias], input=private_key
    )
    assert not result.exit_code, result.output
    assert "SUCCESS" in result.output
    assert test_account.address in result.output
    container.delete_account(non_existing_alias)


def test_list(cli, runner, temp_keyfile_account, existing_alias):
    result = runner.invoke(cli, ["keyring", "accounts", "list"])
    assert temp_keyfile_account.address in result.output
    assert existing_alias in result.output


def test_sign_message(keyring_account):
    eip191message = encode_defunct(text="Hello Test")
    keyring_account.skip_prompt = True
    signature = keyring_account.sign_message(eip191message)
    signature_bytes = signature.encode_rsv()
    signer = Account.recover_message(eip191message, signature=signature_bytes)
    assert signer == keyring_account.address


def test_delete(cli, runner, temp_keyfile_account):
    alias = "alias"
    result = runner.invoke(cli, ["keyring", "accounts", "delete", alias])
    assert f"SUCCESS: Account '{alias}' removed from keying" in result.output

    # Verify account is NOT listed in 'list' command
    result = runner.invoke(cli, ["keyring", "accounts", "list"])
    assert alias not in result.output
