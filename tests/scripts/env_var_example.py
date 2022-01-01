import os

import click


def main():
    actual = os.environ.get("TEST_SECRET")  # Gets set in 'test_secrets.py'
    expected = "this-is-a-test-secret"
    result = "TRUE" if actual == expected else "FALSE"
    click.echo(result)
