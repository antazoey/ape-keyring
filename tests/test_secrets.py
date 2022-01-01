SECRET_KEY = "TEST_SECRET"
SECRET_VALUE = "this-is-a-test-secret"


def test_secrets(cli, runner):
    result = runner.invoke(cli, ["keyring", "secrets", "set", SECRET_KEY], input=SECRET_VALUE)
    assert result.exit_code == 0, result.output

    result = runner.invoke(cli, ["keyring", "secrets", "list"])
    assert SECRET_KEY in result.output

    result = runner.invoke(cli, ["keyring", "secrets", "delete", SECRET_KEY])
    assert result.exit_code == 0, result.output

    result = runner.invoke(cli, ["keyring", "secrets", "list"])
    assert SECRET_KEY not in result.output
