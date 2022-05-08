import pytest

from ape_keyring._secrets import secret_storage

SECRET_KEY = "TEST_SECRET"
SECRET_VALUE = "this-is-a-test-secret"


@pytest.fixture
def temp_secret():
    if SECRET_KEY not in secret_storage.keys:
        secret_storage.store_secret(SECRET_KEY, SECRET_VALUE)

    yield

    if SECRET_KEY in secret_storage.keys:
        secret_storage.delete_secret(SECRET_KEY)


def test_set(cli, runner):
    if SECRET_KEY in secret_storage.keys:
        # Corrupted from previous test.
        secret_storage.delete_secret(SECRET_KEY)

    result = runner.invoke(cli, ["keyring", "secrets", "set", SECRET_KEY], input=SECRET_VALUE)
    assert result.exit_code == 0, result.output


def test_list(cli, runner, temp_secret):
    result = runner.invoke(cli, ["keyring", "secrets", "list"])
    assert SECRET_KEY in result.output


def test_delete(cli, runner, temp_secret):
    result = runner.invoke(cli, ["keyring", "secrets", "delete", SECRET_KEY])
    assert result.exit_code == 0, result.output

    result = runner.invoke(cli, ["keyring", "secrets", "list"])
    assert SECRET_KEY not in result.output
