from ape import accounts
from eth_account import Account
from eth_account.messages import encode_defunct

TEST_ALIAS = "test-alias"


def test_accounts(cli, runner, test_account):
    private_key = test_account._private_key
    result = runner.invoke(cli, ["keyring", "accounts", "import", TEST_ALIAS], input=private_key)
    assert not result.exit_code, result.output
    assert "SUCCESS" in result.output
    assert test_account.address in result.output

    # Verify account is listed in 'list' command
    result = runner.invoke(cli, ["keyring", "accounts", "list"])
    assert test_account.address in result.output
    assert TEST_ALIAS in result.output

    # Verify can sign
    eip191message = encode_defunct(text="Hello Test")
    account = accounts.load(TEST_ALIAS)
    account.skip_prompt = True
    signature = account.sign_message(eip191message)
    signature_bytes = signature.encode_rsv()
    signer = Account.recover_message(eip191message, signature=signature_bytes)
    assert signer == test_account.address

    # Make sure can delete the account
    result = runner.invoke(cli, ["keyring", "accounts", "delete", TEST_ALIAS])
    assert f"SUCCESS: Account '{TEST_ALIAS}' removed from keying" in result.output

    # Verify account is NOT listed in 'list' command
    result = runner.invoke(cli, ["keyring", "accounts", "list"])
    assert test_account.address not in result.output
    assert TEST_ALIAS not in result.output
